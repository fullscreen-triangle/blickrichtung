"""
Spectral Extraction
===================

Extracts 1D spectrum from 2D camera image.
"""

import numpy as np
from typing import Dict, Tuple, Optional
from scipy.ndimage import gaussian_filter1d
from scipy.signal import savgol_filter


class SpectralExtractor:
    """
    Extracts clean 1D spectrum from 2D grating image
    """
    
    def __init__(self):
        """Initialize extractor"""
        pass
        
    def extract_spectrum_1d(self,
                           frame: np.ndarray,
                           roi: Optional[Tuple[int, int, int, int]] = None) -> Dict:
        """
        Extract 1D spectrum from 2D frame
        
        Args:
            frame: 2D image from camera (height, width)
            roi: Region of interest (y_min, y_max, x_min, x_max)
            
        Returns:
            1D spectrum and metadata
        """
        # Apply ROI if specified
        if roi is not None:
            y_min, y_max, x_min, x_max = roi
            frame_roi = frame[y_min:y_max, x_min:x_max]
            x_offset = x_min
        else:
            frame_roi = frame
            x_offset = 0
            
        # Sum along vertical axis (perpendicular to dispersion)
        spectrum_1d = np.sum(frame_roi, axis=0)
        
        # Pixel positions
        pixels = np.arange(len(spectrum_1d)) + x_offset
        
        return {
            'spectrum': spectrum_1d,
            'pixels': pixels,
            'n_pixels': len(spectrum_1d),
            'roi': roi
        }
        
    def baseline_correction(self,
                           spectrum: np.ndarray,
                           method: str = 'rolling_min') -> np.ndarray:
        """
        Remove baseline from spectrum
        
        Args:
            spectrum: Raw spectrum
            method: 'rolling_min', 'polynomial', or 'asymmetric'
            
        Returns:
            Baseline-corrected spectrum
        """
        if method == 'rolling_min':
            # Rolling minimum baseline
            from scipy.ndimage import minimum_filter
            window = len(spectrum) // 10
            baseline = minimum_filter(spectrum, size=window)
            corrected = spectrum - baseline
            
        elif method == 'polynomial':
            # Polynomial baseline
            x = np.arange(len(spectrum))
            # Fit to lower points
            baseline = np.percentile(spectrum, 10)
            mask = spectrum < np.percentile(spectrum, 25)
            coeffs = np.polyfit(x[mask], spectrum[mask], deg=3)
            baseline = np.polyval(coeffs, x)
            corrected = spectrum - baseline
            
        elif method == 'asymmetric':
            # Asymmetric least squares baseline
            corrected = self._asymmetric_least_squares(spectrum)
            
        else:
            raise ValueError(f"Unknown method: {method}")
            
        # Ensure non-negative
        corrected = np.maximum(corrected, 0)
        
        return corrected
        
    def smooth_spectrum(self,
                       spectrum: np.ndarray,
                       method: str = 'savgol',
                       window_size: int = 11) -> np.ndarray:
        """
        Smooth spectrum
        
        Args:
            spectrum: Input spectrum
            method: 'gaussian', 'savgol', or 'boxcar'
            window_size: Smoothing window size
            
        Returns:
            Smoothed spectrum
        """
        if method == 'gaussian':
            sigma = window_size / 4
            smoothed = gaussian_filter1d(spectrum, sigma)
            
        elif method == 'savgol':
            # Savitzky-Golay filter
            order = min(3, window_size - 1)
            smoothed = savgol_filter(spectrum, window_size, order)
            
        elif method == 'boxcar':
            # Simple moving average
            kernel = np.ones(window_size) / window_size
            smoothed = np.convolve(spectrum, kernel, mode='same')
            
        else:
            raise ValueError(f"Unknown method: {method}")
            
        return smoothed
        
    def normalize_spectrum(self,
                          spectrum: np.ndarray,
                          method: str = 'max') -> np.ndarray:
        """
        Normalize spectrum
        
        Args:
            spectrum: Input spectrum
            method: 'max', 'area', or 'reference'
            
        Returns:
            Normalized spectrum
        """
        if method == 'max':
            # Normalize to maximum
            max_val = np.max(spectrum)
            if max_val > 0:
                normalized = spectrum / max_val
            else:
                normalized = spectrum
                
        elif method == 'area':
            # Normalize to unit area
            area = np.trapz(spectrum)
            if area > 0:
                normalized = spectrum / area
            else:
                normalized = spectrum
                
        elif method == 'reference':
            # Normalize to reference wavelength (placeholder)
            normalized = spectrum
            
        else:
            raise ValueError(f"Unknown method: {method}")
            
        return normalized
        
    def process_spectrum_full(self,
                             frame: np.ndarray,
                             roi: Optional[Tuple[int, int, int, int]] = None,
                             baseline_method: str = 'rolling_min',
                             smooth_window: int = 11,
                             normalize: bool = True) -> Dict:
        """
        Complete spectrum processing pipeline
        
        Args:
            frame: 2D camera frame
            roi: Region of interest
            baseline_method: Baseline correction method
            smooth_window: Smoothing window size
            normalize: Whether to normalize
            
        Returns:
            Processed spectrum with all steps
        """
        # Extract 1D
        extraction = self.extract_spectrum_1d(frame, roi)
        spectrum_raw = extraction['spectrum']
        
        # Baseline correction
        spectrum_baseline = self.baseline_correction(
            spectrum_raw,
            method=baseline_method
        )
        
        # Smoothing
        spectrum_smooth = self.smooth_spectrum(
            spectrum_baseline,
            method='savgol',
            window_size=smooth_window
        )
        
        # Normalization
        if normalize:
            spectrum_final = self.normalize_spectrum(
                spectrum_smooth,
                method='max'
            )
        else:
            spectrum_final = spectrum_smooth
            
        return {
            'spectrum_raw': spectrum_raw,
            'spectrum_baseline_corrected': spectrum_baseline,
            'spectrum_smoothed': spectrum_smooth,
            'spectrum_final': spectrum_final,
            'pixels': extraction['pixels'],
            'processing': {
                'baseline_method': baseline_method,
                'smooth_window': smooth_window,
                'normalized': normalize
            }
        }
        
    def _asymmetric_least_squares(self,
                                  y: np.ndarray,
                                  lam: float = 1e6,
                                  p: float = 0.01,
                                  niter: int = 10) -> np.ndarray:
        """
        Asymmetric least squares baseline correction
        
        Args:
            y: Signal
            lam: Smoothness parameter
            p: Asymmetry parameter
            niter: Number of iterations
            
        Returns:
            Baseline-corrected signal
        """
        from scipy.sparse import diags, csr_matrix
        from scipy.sparse.linalg import spsolve
        
        n = len(y)
        D = diags([1, -2, 1], [0, -1, -2], shape=(n, n - 2))
        D = csr_matrix(D)
        
        w = np.ones(n)
        for _ in range(niter):
            W = diags(w, 0, shape=(n, n))
            Z = W + lam * D.dot(D.T)
            z = spsolve(Z, w * y)
            w = p * (y > z) + (1 - p) * (y < z)
            
        # Return corrected
        return y - z
        
    def find_peaks_in_spectrum(self,
                              spectrum: np.ndarray,
                              prominence: float = 0.1) -> Dict:
        """
        Find spectral peaks
        
        Args:
            spectrum: Input spectrum
            prominence: Minimum peak prominence
            
        Returns:
            Peak locations and properties
        """
        from scipy.signal import find_peaks
        
        # Find peaks
        peaks, properties = find_peaks(
            spectrum,
            prominence=prominence * np.max(spectrum),
            width=2
        )
        
        return {
            'peak_positions': peaks,
            'peak_heights': spectrum[peaks],
            'prominences': properties['prominences'],
            'widths': properties['widths'],
            'n_peaks': len(peaks)
        }
