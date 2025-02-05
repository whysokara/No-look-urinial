
#!/usr/bin/env python3

from rich.console import Console
from rich.prompt import IntPrompt, Prompt
from rich.panel import Panel
from rich.text import Text
from typing import List, Set

console = Console()

def validate_total_urinals(value: int) -> bool:
    """Validate the total number of urinals."""
    return 1 <= value <= 20

def validate_occupied_positions(positions: Set[int], total_urinals: int) -> bool:
    """Validate the occupied positions."""
    return all(1 <= pos <= total_urinals for pos in positions)

def parse_occupied_positions(input_str: str, total_urinals: int) -> Set[int]:
    """Parse and validate occupied positions from user input."""
    try:
        # Split input and convert to integers
        positions = {int(pos.strip()) for pos in input_str.split(',') if pos.strip()}
        
        # Validate positions
        if not validate_occupied_positions(positions, total_urinals):
            raise ValueError("Positions must be within valid range")
        
        return positions
    except ValueError as e:
        raise ValueError("Invalid input format. Please use comma-separated numbers.")

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

def display_urinals(total_urinals: int, occupied: Set[int], recommended: int = None) -> None:
    """Display a visual representation of the urinals."""
    urinal_display = ""
    for i in range(1, total_urinals + 1):
        if i in occupied:
            symbol = "🚹"  # Occupied
        elif i == recommended:
            symbol = "✨"  # Recommended
        else:
            symbol = "⬜"  # Empty
        urinal_display += symbol + " "
    
    panel = Panel(
        Text(urinal_display, justify="center"),
        title="Urinal Layout",
        subtitle="🚹=Occupied ⬜=Empty ✨=Recommended"
    )
    console.print(panel)

def main():
    console.print("[bold blue]Welcome to the Optimal Urinal Position Finder![/bold blue]\n")
    
    # Get total number of urinals
    while True:
        try:
            total_urinals = IntPrompt.ask("Enter the total number of urinals (1-20)")
            if not validate_total_urinals(total_urinals):
                console.print("[red]Please enter a number between 1 and 20[/red]")
                continue
            break
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")
    
    # Get occupied positions
    while True:
        try:
            occupied_input = Prompt.ask(
                "Enter occupied positions (comma-separated, e.g., 1,3,5)"
            )
            occupied = parse_occupied_positions(occupied_input, total_urinals)
            if len(occupied) >= total_urinals:
                console.print("[red]All urinals are occupied![/red]")
                continue
            break
        except ValueError as e:
            console.print(f"[red]{str(e)}[/red]")
    
    # Display initial layout
    console.print("\nCurrent layout:")
    display_urinals(total_urinals, occupied)
    
    # Find and display optimal position
    optimal = find_optimal_position(total_urinals, occupied)
    console.print(f"\n[green]Recommended position:[/green] {optimal}")
    console.print("\nFinal layout with recommendation:")
    display_urinals(total_urinals, occupied, optimal)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]An error occurred: {str(e)}[/red]")
