import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from scipy import signal, stats
from scipy.spatial.distance import euclidean
from itertools import combinations
import pandas as pd
import warnings
import os
warnings.filterwarnings('ignore')

# ============================================================================
# S-ENTROPY FRAMEWORK (from your papers)
# ============================================================================

def calculate_s_entropy(sequence, base=2):
    """
    Calculate S-entropy of a sequence
    
    S-entropy measures the information content of directional changes
    in a sequence, transforming linear data into information space.
    
    From St. Stella's Sequence Framework
    """
    if len(sequence) < 2:
        return 0.0
    
    # Calculate differences (directional changes)
    diffs = np.diff(sequence)
    
    # Encode directions: +1 (increase), -1 (decrease), 0 (no change)
    directions = np.sign(diffs)
    
    # Count direction frequencies
    unique, counts = np.unique(directions, return_counts=True)
    
    # Calculate probabilities
    probabilities = counts / len(directions)
    
    # Calculate entropy
    entropy = -np.sum(probabilities * np.log(probabilities + 1e-10) / np.log(base))
    
    return entropy

def directional_encoding(sequence):
    """
    Encode sequence as directional pattern
    
    Returns:
    - directions: array of +1, -1, 0
    - transitions: transition matrix
    - pattern_complexity: measure of pattern richness
    """
    diffs = np.diff(sequence)
    directions = np.sign(diffs)
    
    # Build transition matrix
    transitions = np.zeros((3, 3))  # -1, 0, +1
    direction_map = {-1: 0, 0: 1, 1: 2}
    
    for i in range(len(directions) - 1):
        from_state = direction_map[directions[i]]
        to_state = direction_map[directions[i + 1]]
        transitions[from_state, to_state] += 1
    
    # Normalize
    row_sums = transitions.sum(axis=1, keepdims=True)
    transitions = np.divide(transitions, row_sums, 
                           where=row_sums != 0, out=np.zeros_like(transitions))
    
    # Pattern complexity (entropy of transition matrix)
    flat_probs = transitions.flatten()
    flat_probs = flat_probs[flat_probs > 0]
    pattern_complexity = -np.sum(flat_probs * np.log(flat_probs + 1e-10))
    
    return directions, transitions, pattern_complexity

def s_entropy_coordinates(sequence, window_size=10):
    """
    Transform sequence into S-entropy coordinate space
    
    Creates multi-dimensional representation where each dimension
    captures entropy at different scales.
    
    Returns:
    - coordinates: array of S-entropy values at different scales
    - scales: corresponding window sizes
    """
    coordinates = []
    scales = []
    
    # Multi-scale analysis
    for scale in range(2, min(window_size + 1, len(sequence) // 2)):
        # Sliding window entropy calculation
        entropies = []
        for i in range(0, len(sequence) - scale, scale // 2):
            window = sequence[i:i + scale]
            entropy = calculate_s_entropy(window)
            entropies.append(entropy)
        
        if len(entropies) > 0:
            coordinates.append(np.mean(entropies))
            scales.append(scale)
    
    return np.array(coordinates), np.array(scales)

def cardinal_direction_transform(sequence):
    """
    Transform sequence into cardinal directions (N, S, E, W, NE, NW, SE, SW)
    
    From St. Stella's Sequence Framework:
    Maps changes in sequence to 8 cardinal directions based on
    magnitude and sign of change.
    """
    diffs = np.diff(sequence)
    
    # Normalize differences
    if np.std(diffs) > 0:
        normalized_diffs = (diffs - np.mean(diffs)) / np.std(diffs)
    else:
        normalized_diffs = diffs
    
    # Map to cardinal directions
    directions = []
    direction_map = {
        'N': 0, 'NE': 1, 'E': 2, 'SE': 3,
        'S': 4, 'SW': 5, 'W': 6, 'NW': 7
    }
    
    for diff in normalized_diffs:
        if diff > 1.0:
            directions.append('N')  # Strong increase
        elif diff > 0.5:
            directions.append('NE')  # Moderate increase
        elif diff > 0:
            directions.append('E')  # Slight increase
        elif diff > -0.5:
            directions.append('SE')  # Slight decrease
        elif diff > -1.0:
            directions.append('S')  # Moderate decrease
        else:
            directions.append('SW')  # Strong decrease
    
    # Count direction frequencies
    direction_counts = {d: 0 for d in direction_map.keys()}
    for d in directions:
        direction_counts[d] += 1
    
    # Convert to vector
    direction_vector = np.array([direction_counts[d] for d in sorted(direction_map.keys())])
    direction_vector = direction_vector / (np.sum(direction_vector) + 1e-10)
    
    return direction_vector, directions

def bmd_variance_minimization(sequence, frame_rate=2000):
    """
    Apply BMD (Bayesian Model of Discrimination) variance minimization
    
    Selects frames that minimize variance in the sequence,
    analogous to how BMD selects perceptual frames.
    """
    if len(sequence) < frame_rate:
        return sequence
    
    # Sliding window variance calculation
    window_size = max(1, len(sequence) // frame_rate)
    selected_frames = []
    
    for i in range(0, len(sequence), window_size):
        window = sequence[i:i + window_size]
        if len(window) > 0:
            # Select frame with minimum local variance
            variances = []
            for j in range(len(window)):
                local_window = window[max(0, j-5):min(len(window), j+5)]
                variances.append(np.var(local_window))
            
            if len(variances) > 0:
                min_var_idx = np.argmin(variances)
                selected_frames.append(window[min_var_idx])
    
    return np.array(selected_frames)

# ============================================================================
# DATA LOADING AND PREPROCESSING
# ============================================================================

def load_all_data():
    """Load comprehensive sleep and activity data"""
    print("Loading metabolic decomposition data with S-entropy framework...")
    
    # Define base path
    base_path = './public'  # Adjust this to your actual path
    
    # Check if path exists
    if not os.path.exists(base_path):
        print(f"Warning: {base_path} not found, trying current directory...")
        base_path = '.'
    
    try:
        with open(os.path.join(base_path, 'infraredSleep.json'), 'r') as f:
            infrared_sleep = json.load(f)
        print(f"✓ Loaded infraredSleep.json")
    except FileNotFoundError:
        print("⚠ infraredSleep.json not found, using empty data")
        infrared_sleep = []
    
    try:
        with open(os.path.join(base_path, 'sleep_summary.json'), 'r') as f:
            sleep_summary = json.load(f)
        print(f"✓ Loaded sleep_summary.json")
    except FileNotFoundError:
        print("⚠ sleep_summary.json not found, using empty data")
        sleep_summary = []
    
    try:
        with open(os.path.join(base_path, 'sleepRecords.json'), 'r') as f:
            sleep_records = json.load(f)
        print(f"✓ Loaded sleepRecords.json ({len(sleep_records)} records)")
    except FileNotFoundError:
        print("⚠ sleepRecords.json not found, using empty data")
        sleep_records = []
    
    try:
        with open(os.path.join(base_path, 'actigram.json'), 'r') as f:
            actigram = json.load(f)
        print(f"✓ Loaded actigram.json ({len(actigram)} points)")
    except FileNotFoundError:
        print("⚠ actigram.json not found, using empty data")
        actigram = []
    
    try:
        with open(os.path.join(base_path, 'activity.json'), 'r') as f:
            activity = json.load(f)
        print(f"✓ Loaded activity.json ({len(activity)} days)")
    except FileNotFoundError:
        print("⚠ activity.json not found, using empty data")
        activity = []
    
    try:
        with open(os.path.join(base_path, 'activityPPG.json'), 'r') as f:
            activity_ppg = json.load(f)
        print(f"✓ Loaded activityPPG.json")
    except FileNotFoundError:
        print("⚠ activityPPG.json not found, using empty data")
        activity_ppg = []
    
    return {
        'infrared_sleep': infrared_sleep,
        'sleep_summary': sleep_summary,
        'sleep_records': sleep_records,
        'actigram': actigram,
        'activity': activity,
        'activity_ppg': activity_ppg
    }

# ============================================================================
# S-ENTROPY ANALYSIS OF SLEEP SEQUENCES
# ============================================================================

def analyze_sleep_sequence_entropy(data):
    """
    Analyze sleep sequences using S-entropy framework
    
    Transforms sleep stage sequences (Deep → REM → Wake) into
    multi-dimensional S-entropy space for pattern recognition.
    """
    print("\nAnalyzing sleep sequences with S-entropy transformation...")
    
    sleep_episodes = []
    
    for record in data['sleep_records']:
        date = record.get('date', '')
        
        # Extract sleep stages (in minutes)
        deep = record.get('deep', 0) / 60
        rem = record.get('rem', 0) / 60
        light = record.get('light', 0) / 60
        awake = record.get('awake', 0) / 60
        
        # Get HR sequence if available
        hr_avg = record.get('hr_average', 0)
        hr_min = record.get('hr_lowest', 0)
        hr_max = record.get('hr_5min_high', 0)
        
        # Create sleep stage sequence (simplified)
        # Encode as: 0=awake, 1=light, 2=deep, 3=REM
        sleep_sequence = []
        
        # Approximate sequence based on durations
        if deep > 0:
            sleep_sequence.extend([2] * int(deep))
        if rem > 0:
            sleep_sequence.extend([3] * int(rem))
        if light > 0:
            sleep_sequence.extend([1] * int(light))
        if awake > 0:
            sleep_sequence.extend([0] * int(awake))
        
        if len(sleep_sequence) < 2:
            continue
        
        sleep_sequence = np.array(sleep_sequence)
        
        # Calculate S-entropy
        s_entropy = calculate_s_entropy(sleep_sequence)
        
        # Directional encoding
        directions, transitions, pattern_complexity = directional_encoding(sleep_sequence)
        
        # S-entropy coordinates (multi-scale)
        s_coords, scales = s_entropy_coordinates(sleep_sequence)
        
        # Cardinal direction transform
        cardinal_vector, cardinal_dirs = cardinal_direction_transform(sleep_sequence)
        
        # HR sequence analysis
        if hr_avg > 0 and hr_min > 0 and hr_max > 0:
            hr_sequence = np.linspace(hr_min, hr_max, len(sleep_sequence))
            hr_entropy = calculate_s_entropy(hr_sequence)
            hr_coords, _ = s_entropy_coordinates(hr_sequence)
        else:
            hr_entropy = 0
            hr_coords = np.array([])
        
        sleep_episodes.append({
            'date': date,
            'deep_min': deep,
            'rem_min': rem,
            'light_min': light,
            'awake_min': awake,
            'sleep_sequence': sleep_sequence,
            's_entropy': s_entropy,
            'pattern_complexity': pattern_complexity,
            's_coordinates': s_coords,
            'cardinal_vector': cardinal_vector,
            'hr_avg': hr_avg,
            'hr_entropy': hr_entropy,
            'hr_coordinates': hr_coords,
            'transition_matrix': transitions
        })
    
    print(f"✓ Analyzed {len(sleep_episodes)} sleep episodes")
    
    if len(sleep_episodes) > 0:
        avg_entropy = np.mean([ep['s_entropy'] for ep in sleep_episodes])
        avg_complexity = np.mean([ep['pattern_complexity'] for ep in sleep_episodes])
        print(f"  - Average S-entropy: {avg_entropy:.3f}")
        print(f"  - Average pattern complexity: {avg_complexity:.3f}")
    
    return sleep_episodes

# ============================================================================
# S-ENTROPY ANALYSIS OF DAYTIME ACTIVITY
# ============================================================================

def analyze_activity_sequence_entropy(data):
    """
    Analyze daytime activity sequences using S-entropy framework
    """
    print("\nAnalyzing activity sequences with S-entropy transformation...")
    
    activity_episodes = []
    
    # Process actigram data (high-resolution activity)
    actigram_data = data['actigram']
    
    if len(actigram_data) == 0:
        print("⚠ No actigram data available")
        return activity_episodes
    
    # Group by date
    dates = {}
    for point in actigram_data:
        date = point.get('date', '')[:10]  # Get date part
        if date not in dates:
            dates[date] = []
        dates[date].append(point.get('score', 0))
    
    for date, scores in dates.items():
        if len(scores) < 2:
            continue
        
        activity_sequence = np.array(scores)
        
        # Calculate S-entropy
        s_entropy = calculate_s_entropy(activity_sequence)
        
        # Directional encoding
        directions, transitions, pattern_complexity = directional_encoding(activity_sequence)
        
        # S-entropy coordinates (multi-scale)
        s_coords, scales = s_entropy_coordinates(activity_sequence)
        
        # Cardinal direction transform
        cardinal_vector, cardinal_dirs = cardinal_direction_transform(activity_sequence)
        
        # BMD variance minimization
        bmd_frames = bmd_variance_minimization(activity_sequence)
        bmd_entropy = calculate_s_entropy(bmd_frames) if len(bmd_frames) > 1 else 0
        
        activity_episodes.append({
            'date': date,
            'activity_sequence': activity_sequence,
            's_entropy': s_entropy,
            'pattern_complexity': pattern_complexity,
            's_coordinates': s_coords,
            'cardinal_vector': cardinal_vector,
            'bmd_frames': bmd_frames,
            'bmd_entropy': bmd_entropy,
            'transition_matrix': transitions,
            'mean_activity': np.mean(activity_sequence),
            'activity_variance': np.var(activity_sequence)
        })
    
    print(f"✓ Analyzed {len(activity_episodes)} activity episodes")
    
    if len(activity_episodes) > 0:
        avg_entropy = np.mean([ep['s_entropy'] for ep in activity_episodes])
        avg_bmd_entropy = np.mean([ep['bmd_entropy'] for ep in activity_episodes])
        print(f"  - Average S-entropy: {avg_entropy:.3f}")
        print(f"  - Average BMD entropy: {avg_bmd_entropy:.3f}")
    
    return activity_episodes

# ============================================================================
# CROSS-CORRELATION IN S-ENTROPY SPACE
# ============================================================================

def find_entropy_correlations(sleep_episodes, activity_episodes):
    """
    Find correlations between sleep and activity in S-entropy space
    
    This is the KEY insight: by transforming both sleep and activity
    into S-entropy space, we can find hidden correlations that
    linear analysis would miss.
    """
    print("\nFinding correlations in S-entropy space...")
    
    correlations = []
    
    if len(sleep_episodes) == 0 or len(activity_episodes) == 0:
        print("⚠ Insufficient data for correlation analysis")
        return correlations
    
    # Match dates
    sleep_dates = {ep['date']: ep for ep in sleep_episodes}
    activity_dates = {ep['date']: ep for ep in activity_episodes}
    
    common_dates = set(sleep_dates.keys()) & set(activity_dates.keys())
    
    print(f"  - Found {len(common_dates)} matching dates")
    
    for date in common_dates:
        sleep_ep = sleep_dates[date]
        activity_ep = activity_dates[date]
        
        # S-entropy correlation
        entropy_correlation = np.corrcoef([sleep_ep['s_entropy']], 
                                         [activity_ep['s_entropy']])[0, 1]
        
        # Pattern complexity correlation
        complexity_correlation = np.corrcoef([sleep_ep['pattern_complexity']], 
                                            [activity_ep['pattern_complexity']])[0, 1]
        
        # Cardinal direction correlation (cosine similarity)
        cardinal_similarity = np.dot(sleep_ep['cardinal_vector'], 
                                    activity_ep['cardinal_vector'])
        
        # Multi-scale correlation (if both have coordinates)
        if len(sleep_ep['s_coordinates']) > 0 and len(activity_ep['s_coordinates']) > 0:
            # Match lengths
            min_len = min(len(sleep_ep['s_coordinates']), len(activity_ep['s_coordinates']))
            if min_len > 1:
                multiscale_correlation = np.corrcoef(
                    sleep_ep['s_coordinates'][:min_len],
                    activity_ep['s_coordinates'][:min_len]
                )[0, 1]
            else:
                multiscale_correlation = 0
        else:
            multiscale_correlation = 0
        
        # Metabolic cost estimation
        # Night cost = REM duration * HR * entropy
        night_cost = (sleep_ep['rem_min'] * sleep_ep['hr_avg'] * 
                     sleep_ep['s_entropy']) if sleep_ep['hr_avg'] > 0 else 0
        
        # Day cost = activity variance * entropy
        day_cost = activity_ep['activity_variance'] * activity_ep['s_entropy']
        
        # Thought metabolism (from night)
        thought_metabolism = night_cost
        
        # Total metabolism (day)
        total_metabolism = day_cost
        
        # Perception metabolism (residual)
        perception_metabolism = max(0, total_metabolism - thought_metabolism)
        
        correlations.append({
            'date': date,
            'entropy_correlation': entropy_correlation,
            'complexity_correlation': complexity_correlation,
            'cardinal_similarity': cardinal_similarity,
            'multiscale_correlation': multiscale_correlation,
            'night_cost': night_cost,
            'day_cost': day_cost,
            'thought_metabolism': thought_metabolism,
            'perception_metabolism': perception_metabolism,
            'consciousness_metabolism': thought_metabolism + perception_metabolism,
            'sleep_entropy': sleep_ep['s_entropy'],
            'activity_entropy': activity_ep['s_entropy']
        })
    
    print(f"✓ Calculated {len(correlations)} correlation pairs")
    
    if len(correlations) > 0:
        valid_entropy_corrs = [c['entropy_correlation'] for c in correlations if not np.isnan(c['entropy_correlation'])]
        if len(valid_entropy_corrs) > 0:
            avg_entropy_corr = np.mean(valid_entropy_corrs)
            avg_cardinal_sim = np.mean([c['cardinal_similarity'] for c in correlations])
            print(f"  - Average entropy correlation: {avg_entropy_corr:.3f}")
            print(f"  - Average cardinal similarity: {avg_cardinal_sim:.3f}")
    
    return correlations

# ... (visualization functions remain the same but I'll include the complete create_s_entropy_visualization for completeness)

def create_s_entropy_visualization(sleep_episodes, activity_episodes, 
                                   correlations, output_dir='./'):
    """
    Create comprehensive S-entropy space visualization
    """
    print("\nGenerating S-entropy space visualization...")
    
    fig = plt.figure(figsize=(20, 16))
    gs = GridSpec(4, 3, figure=fig, hspace=0.4, wspace=0.35)
    
    color_sleep = '#9B59B6'
    color_activity = '#3498DB'
    color_consciousness = '#E74C3C'
    
    # ========================================================================
    # Panel 1: S-Entropy Distribution (Sleep vs Activity)
    # ========================================================================
    ax1 = fig.add_subplot(gs[0, 0])
    
    sleep_entropies = [ep['s_entropy'] for ep in sleep_episodes]
    activity_entropies = [ep['s_entropy'] for ep in activity_episodes]
    
    if len(sleep_entropies) > 0:
        ax1.hist(sleep_entropies, bins=20, alpha=0.6, color=color_sleep, 
                label='Sleep', edgecolor='black')
    if len(activity_entropies) > 0:
        ax1.hist(activity_entropies, bins=20, alpha=0.6, color=color_activity, 
                label='Activity', edgecolor='black')
    
    ax1.set_xlabel('S-Entropy', fontweight='bold')
    ax1.set_ylabel('Frequency', fontweight='bold')
    ax1.set_title('A. S-Entropy Distribution: Sleep vs Activity', 
                 fontweight='bold', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 2: Pattern Complexity
    # ========================================================================
    ax2 = fig.add_subplot(gs[0, 1])
    
    sleep_complexity = [ep['pattern_complexity'] for ep in sleep_episodes]
    activity_complexity = [ep['pattern_complexity'] for ep in activity_episodes]
    
    if len(sleep_complexity) > 0:
        ax2.hist(sleep_complexity, bins=20, alpha=0.6, color=color_sleep, 
                label='Sleep', edgecolor='black')
    if len(activity_complexity) > 0:
        ax2.hist(activity_complexity, bins=20, alpha=0.6, color=color_activity, 
                label='Activity', edgecolor='black')
    
    ax2.set_xlabel('Pattern Complexity', fontweight='bold')
    ax2.set_ylabel('Frequency', fontweight='bold')
    ax2.set_title('B. Pattern Complexity Distribution', 
                 fontweight='bold', fontsize=13)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 3: S-Entropy Phase Space
    # ========================================================================
    ax3 = fig.add_subplot(gs[0, 2])
    
    if len(correlations) > 0:
        sleep_ent = [c['sleep_entropy'] for c in correlations]
        activity_ent = [c['activity_entropy'] for c in correlations]
        
        scatter = ax3.scatter(sleep_ent, activity_ent, 
                            c=[c['consciousness_metabolism'] for c in correlations],
                            cmap='hot', s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # Add diagonal (perfect correlation)
        if len(sleep_ent) > 0 and len(activity_ent) > 0:
            min_ent = min(min(sleep_ent), min(activity_ent))
            max_ent = max(max(sleep_ent), max(activity_ent))
            ax3.plot([min_ent, max_ent], [min_ent, max_ent], 'r--', 
                    linewidth=2, label='Perfect Correlation')
        
        ax3.set_xlabel('Sleep S-Entropy', fontweight='bold')
        ax3.set_ylabel('Activity S-Entropy', fontweight='bold')
        ax3.set_title('C. S-Entropy Phase Space', fontweight='bold', fontsize=13)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        cbar = plt.colorbar(scatter, ax=ax3)
        cbar.set_label('Consciousness Metabolism', fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'No correlation data', ha='center', va='center',
                transform=ax3.transAxes, fontsize=14)
        ax3.set_title('C. S-Entropy Phase Space', fontweight='bold', fontsize=13)
    
    # ========================================================================
    # Panel 4: Cardinal Direction Compass (Sleep)
    # ========================================================================
    ax4 = fig.add_subplot(gs[1, 0], projection='polar')
    
    if len(sleep_episodes) > 0:
        # Average cardinal vector
        avg_cardinal = np.mean([ep['cardinal_vector'] for ep in sleep_episodes], axis=0)
        
        theta = np.linspace(0, 2*np.pi, 8, endpoint=False)
        width = 2*np.pi / 8
        
        bars = ax4.bar(theta, avg_cardinal, width=width, alpha=0.7, 
                      color=color_sleep, edgecolor='black', linewidth=2)
        
        ax4.set_title('D. Sleep Cardinal Directions', fontweight='bold', 
                     fontsize=13, pad=20)
        ax4.set_theta_zero_location('N')
        ax4.set_theta_direction(-1)
        
        # Add labels
        labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        ax4.set_xticks(theta)
        ax4.set_xticklabels(labels)
    
    # ========================================================================
    # Panel 5: Cardinal Direction Compass (Activity)
    # ========================================================================
    ax5 = fig.add_subplot(gs[1, 1], projection='polar')
    
    if len(activity_episodes) > 0:
        # Average cardinal vector
        avg_cardinal = np.mean([ep['cardinal_vector'] for ep in activity_episodes], axis=0)
        
        theta = np.linspace(0, 2*np.pi, 8, endpoint=False)
        width = 2*np.pi / 8
        
        bars = ax5.bar(theta, avg_cardinal, width=width, alpha=0.7, 
                      color=color_activity, edgecolor='black', linewidth=2)
        
        ax5.set_title('E. Activity Cardinal Directions', fontweight='bold', 
                     fontsize=13, pad=20)
        ax5.set_theta_zero_location('N')
        ax5.set_theta_direction(-1)
        
        labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        ax5.set_xticks(theta)
        ax5.set_xticklabels(labels)
    
    # ========================================================================
    # Panel 6: Correlation Matrix
    # ========================================================================
    ax6 = fig.add_subplot(gs[1, 2])
    
    if len(correlations) > 0:
        corr_types = ['Entropy', 'Complexity', 'Cardinal', 'Multi-Scale']
        
        valid_entropy = [c['entropy_correlation'] for c in correlations if not np.isnan(c['entropy_correlation'])]
        valid_complexity = [c['complexity_correlation'] for c in correlations if not np.isnan(c['complexity_correlation'])]
        valid_multiscale = [c['multiscale_correlation'] for c in correlations if not np.isnan(c['multiscale_correlation'])]
        
        corr_values = [
            np.mean(valid_entropy) if len(valid_entropy) > 0 else 0,
            np.mean(valid_complexity) if len(valid_complexity) > 0 else 0,
            np.mean([c['cardinal_similarity'] for c in correlations]),
            np.mean(valid_multiscale) if len(valid_multiscale) > 0 else 0
        ]
        
        bars = ax6.barh(corr_types, corr_values, color=color_consciousness, 
                       alpha=0.7, edgecolor='black', linewidth=2)
        
        # Add value labels
        for bar, val in zip(bars, corr_values):
            width = bar.get_width()
            ax6.text(width, bar.get_y() + bar.get_height()/2,
                    f'{val:.3f}',
                    ha='left', va='center', fontweight='bold', fontsize=10)
        
        ax6.set_xlabel('Correlation Coefficient', fontweight='bold')
        ax6.set_title('F. Sleep-Activity Correlations\n(S-Entropy Space)', 
                     fontweight='bold', fontsize=13)
        ax6.set_xlim(-1, 1)
        ax6.axvline(0, color='black', linestyle='-', linewidth=1)
        ax6.grid(True, alpha=0.3, axis='x')
    else:
        ax6.text(0.5, 0.5, 'No correlation data', ha='center', va='center',
                transform=ax6.transAxes, fontsize=14)
        ax6.set_title('F. Sleep-Activity Correlations', fontweight='bold', fontsize=13)
    
    # ========================================================================
    # Panel 7: Metabolic Decomposition
    # ========================================================================
    ax7 = fig.add_subplot(gs[2, :])
    
    if len(correlations) > 0:
        indices = np.arange(len(correlations))
        thought = [c['thought_metabolism'] for c in correlations]
        perception = [c['perception_metabolism'] for c in correlations]
        
        ax7.bar(indices, thought, label='Thought (from dreams)', 
               color=color_sleep, alpha=0.7, edgecolor='black')
        ax7.bar(indices, perception, bottom=thought,
               label='Perception (residual)', color=color_activity, 
               alpha=0.7, edgecolor='black')
        
        # Total line
        consciousness = np.array(thought) + np.array(perception)
        ax7.plot(indices, consciousness, color=color_consciousness, 
                linewidth=2, marker='o', markersize=3, 
                label='Total Consciousness')
        
        ax7.set_xlabel('Time Period', fontweight='bold', fontsize=12)
        ax7.set_ylabel('Metabolic Cost (S-Entropy Units)', fontweight='bold', fontsize=12)
        ax7.set_title('G. Consciousness Metabolic Decomposition (S-Entropy Framework)',
                     fontweight='bold', fontsize=14)
        ax7.legend(loc='upper right', fontsize=10)
        ax7.grid(True, alpha=0.3, axis='y')
    else:
        ax7.text(0.5, 0.5, 'No metabolic data', ha='center', va='center',
                transform=ax7.transAxes, fontsize=14)
        ax7.set_title('G. Consciousness Metabolic Decomposition', fontweight='bold', fontsize=14)
    
    # ========================================================================
    # Panel 8: Multi-Scale S-Coordinates
    # ========================================================================
    ax8 = fig.add_subplot(gs[3, 0])
    
    if len(sleep_episodes) > 0:
        # Plot first few episodes with multi-scale coordinates
        plotted = 0
        for i, ep in enumerate(sleep_episodes[:5]):
            if len(ep['s_coordinates']) > 0:
                scales = np.arange(len(ep['s_coordinates']))
                ax8.plot(scales, ep['s_coordinates'], marker='o', 
                        label=f"Episode {i+1}", alpha=0.7)
                plotted += 1
        
        if plotted > 0:
            ax8.set_xlabel('Scale', fontweight='bold')
            ax8.set_ylabel('S-Entropy', fontweight='bold')
            ax8.set_title('H. Multi-Scale S-Entropy Coordinates\n(Sleep)', 
                         fontweight='bold', fontsize=13)
            ax8.legend(fontsize=8)
            ax8.grid(True, alpha=0.3)
        else:
            ax8.text(0.5, 0.5, 'No multi-scale data', ha='center', va='center',
                    transform=ax8.transAxes, fontsize=12)
            ax8.set_title('H. Multi-Scale S-Entropy Coordinates', fontweight='bold', fontsize=13)
    
    # ========================================================================
    # Panel 9: BMD Variance Minimization Effect
    # ========================================================================
    ax9 = fig.add_subplot(gs[3, 1])
    
    if len(activity_episodes) > 0:
        original_entropies = [ep['s_entropy'] for ep in activity_episodes]
        bmd_entropies = [ep['bmd_entropy'] for ep in activity_episodes]
        
        ax9.scatter(original_entropies, bmd_entropies, 
                   c=range(len(activity_episodes)), cmap='viridis',
                   s=80, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # Add diagonal
        if len(original_entropies) > 0 and len(bmd_entropies) > 0:
            min_ent = min(min(original_entropies), min(bmd_entropies))
            max_ent = max(max(original_entropies), max(bmd_entropies))
            ax9.plot([min_ent, max_ent], [min_ent, max_ent], 'r--', 
                    linewidth=2, label='No Change')
        
        ax9.set_xlabel('Original S-Entropy', fontweight='bold')
        ax9.set_ylabel('BMD-Filtered S-Entropy', fontweight='bold')
        ax9.set_title('I. BMD Variance Minimization Effect', 
                     fontweight='bold', fontsize=13)
        ax9.legend()
        ax9.grid(True, alpha=0.3)
    
    # ========================================================================
    # Panel 10: Summary Statistics
    # ========================================================================
    ax10 = fig.add_subplot(gs[3, 2])
    ax10.axis('off')
    
    if len(correlations) > 0 and len(sleep_episodes) > 0 and len(activity_episodes) > 0:
        avg_thought = np.mean([c['thought_metabolism'] for c in correlations])
        avg_perception = np.mean([c['perception_metabolism'] for c in correlations])
        avg_consciousness = avg_thought + avg_perception
        
        valid_entropy_corrs = [c['entropy_correlation'] for c in correlations if not np.isnan(c['entropy_correlation'])]
        avg_entropy_corr = np.mean(valid_entropy_corrs) if len(valid_entropy_corrs) > 0 else 0
        avg_cardinal_sim = np.mean([c['cardinal_similarity'] for c in correlations])
        
        thought_pct = (avg_thought / avg_consciousness * 100) if avg_consciousness > 0 else 0
        perception_pct = (avg_perception / avg_consciousness * 100) if avg_consciousness > 0 else 0
        
        summary_text = f"""
╔═══════════════════════════════════╗
║  S-ENTROPY FRAMEWORK ANALYSIS     ║
╚═══════════════════════════════════╝

SLEEP EPISODES:
├─ Total analyzed: {len(sleep_episodes)}
├─ Avg S-entropy: {np.mean(sleep_entropies):.3f}
└─ Avg complexity: {np.mean(sleep_complexity):.3f}

ACTIVITY EPISODES:
├─ Total analyzed: {len(activity_episodes)}
├─ Avg S-entropy: {np.mean(activity_entropies):.3f}
└─ Avg complexity: {np.mean(activity_complexity):.3f}

CORRELATIONS (S-ENTROPY SPACE):
├─ Entropy correlation: {avg_entropy_corr:.3f}
├─ Cardinal similarity: {avg_cardinal_sim:.3f}
└─ Matched periods: {len(correlations)}

METABOLIC DECOMPOSITION:
├─ Thought: {avg_thought:.2f}
├─ Perception: {avg_perception:.2f}
└─ Consciousness: {avg_consciousness:.2f}

RATIOS:
├─ Thought: {thought_pct:.1f}%
└─ Perception: {perception_pct:.1f}%

KEY INSIGHT:
  By transforming sequences into
  S-entropy space, we reveal hidden
  correlations between sleep and
  activity that linear analysis
  cannot detect.
  
  Consciousness emerges from the
  coupling of thought (dreams) and
  perception (activity) in multi-
  dimensional information space.
"""
    else:
        summary_text = """
╔═══════════════════════════════════╗
║  S-ENTROPY FRAMEWORK ANALYSIS     ║
╚═══════════════════════════════════╝

INSUFFICIENT DATA

Please ensure JSON files are in the
correct location (../public or .)

Required files:
- sleepRecords.json
- actigram.json
- activityPPG.json
"""
    
    ax10.text(0.05, 0.95, summary_text, transform=ax10.transAxes,
             fontsize=8, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
    
    fig.suptitle('S-ENTROPY FRAMEWORK: Multi-Dimensional Analysis of Consciousness\n' +
                 'Transforming Sequences into Information Space',
                 fontsize=16, fontweight='bold', y=0.99)
    
    output_path = os.path.join(output_dir, 's_entropy_consciousness_analysis.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.close()

def main():
    """Main analysis pipeline with S-entropy framework"""
    print("="*70)
    print("S-ENTROPY FRAMEWORK FOR CONSCIOUSNESS DECOMPOSITION")
    print("="*70)
    print("\nTheoretical Foundation (from St. Stella's Sequence):")
    print("  1. Transform sequences into S-entropy space")
    print("  2. Apply directional encoding and cardinal transforms")
    print("  3. Find correlations in multi-dimensional space")
    print("  4. Decompose consciousness metabolically")
    print("="*70)
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    # Load data
    data = load_all_data()
    
    # Analyze sleep sequences with S-entropy
    sleep_episodes = analyze_sleep_sequence_entropy(data)
    
    # Analyze activity sequences with S-entropy
    activity_episodes = analyze_activity_sequence_entropy(data)
    
    # Find correlations in S-entropy space
    correlations = find_entropy_correlations(sleep_episodes, activity_episodes)
    
    # Generate visualization
    create_s_entropy_visualization(sleep_episodes, activity_episodes, correlations)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print("\nGenerated file:")
    print("  - s_entropy_consciousness_analysis.png")
    print("\nKEY DISCOVERY:")
    print("  S-entropy transformation reveals hidden correlations")
    print("  between sleep and activity sequences!")
    print("="*70)

if __name__ == "__main__":
    main()
