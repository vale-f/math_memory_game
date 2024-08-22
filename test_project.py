import pytest
from project import Card, create_board_operations, create_board_results, center_cards_horizontally

# Test the creation of board operations
def test_create_board_operations():
    board_operations = create_board_operations()

    # Verify that the board has exactly 12 cards
    assert len(board_operations) == 12, "Board should have 12 cards"

    # Ensure that each card is an instance of the Card class
    for card in board_operations:
        assert isinstance(card, Card), f"Got unexpected type: {type(card)}"

        # Check that the card contains a valid arithmetic expression
        parts = card.text.split()
        assert len(parts) == 3, f"Unexpected format in card text: {card.text}"
        assert parts[0].isdigit(), f"First part is not a digit: {parts[0]}"
        assert parts[2].isdigit(), f"Third part is not a digit: {parts[2]}"
        assert parts[1] in ['+', '-', '*', '/'], f"Invalid operator: {parts[1]}"

# Test the creation of board results
def test_create_board_results():
    board_operations = create_board_operations()
    board_results = create_board_results(board_operations)

    # Verify that the board results have exactly 12 cards
    assert len(board_results) == 12, "Board results should have 12 cards"

    # Ensure that each result card is an instance of the Card class
    for card in board_results:
        assert isinstance(card, Card), f"Unexpected format in card text: {type(card)}"

        # Validate that the result is either an integer, a rounded float, or 'Inf'
        text = card.text
        if text != 'Inf':
            try:
                result_value = float(text)
                if result_value.is_integer():
                    result_value = int(result_value)
            except ValueError:
                pytest.fail(f"Card text '{text}' is not a valid number")

# Test the horizontal centering of cards
def test_center_cards_horizontally():
    cards = create_board_operations()
    initial_x_positions = [card.rect.x for card in cards]
    start_x = 50

    center_cards_horizontally(cards, start_x)

    # Check that each card's x position has been correctly adjusted
    for i, card in enumerate(cards):
        assert card.rect.x == initial_x_positions[i] + start_x, (
            f"Card {i} x-position should be {initial_x_positions[i] + start_x}, but it's currently at {card.rect.x}"
        )
