from flask import Flask, render_template, request, jsonify
from typing import List, Set

app = Flask(__name__)

def validate_total_urinals(value: int) -> bool:
    """Validate the total number of urinals."""
    return 1 <= value <= 20

def validate_occupied_positions(positions: Set[int], total_urinals: int) -> bool:
    """Validate the occupied positions."""
    return all(1 <= pos <= total_urinals for pos in positions)

def find_optimal_position(total_urinals: int, occupied: Set[int]) -> int:
    """Find the optimal urinal position."""
    if not occupied:
        return 1  # If none occupied, take the first position
    
    max_min_distance = 0
    optimal_position = -1
    
    # Try each available position
    for pos in range(1, total_urinals + 1):
        if pos in occupied:
            continue
            
        # Calculate minimum distance to any occupied urinal
        min_distance = float('inf')
        for occ in occupied:
            distance = abs(pos - occ)
            min_distance = min(min_distance, distance)
        
        # Update optimal position if this position has a better minimum distance
        if min_distance > max_min_distance:
            max_min_distance = min_distance
            optimal_position = pos
    
    return optimal_position

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        total_urinals = int(data['totalUrinals'])
        occupied = set(map(int, data['occupied']))

        if not validate_total_urinals(total_urinals):
            return jsonify({'error': 'Total urinals must be between 1 and 20'}), 400

        if not validate_occupied_positions(occupied, total_urinals):
            return jsonify({'error': 'Invalid occupied positions'}), 400

        if len(occupied) >= total_urinals:
            return jsonify({'error': 'All urinals are occupied!'}), 400

        optimal = find_optimal_position(total_urinals, occupied)
        return jsonify({
            'optimal': optimal,
            'total': total_urinals,
            'occupied': list(occupied)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
