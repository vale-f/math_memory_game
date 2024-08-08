import pytest
from project import Card, create_board_operations, create_board_results, center_cards_horizontally

def test_create_board_operations():
    board_operations = create_board_operations()

    # Check that the board has 12 cards
    assert len(board_operations) == 12

    # Check that each card is an instance of Card
    assert all(isinstance(card, Card) for card in board_operations)

    # Check that each card has a valid arithmetic expression
    for card in board_operations:
        text = card.text
        parts = text.split()
        assert len(parts) == 3
        assert parts[0].isdigit()
        assert parts[2].isdigit()
        assert parts[1] in ['+', '-', '*', '/']

def test_create_board_results():
    board_operations = create_board_operations()
    board_results = create_board_results(board_operations)

    # Check that the board has 12 cards
    assert len(board_results) == 12

    # Check that each card is an instance of Card
    assert all(isinstance(card, Card) for card in board_results)

    # Check that each card has a valid result (either an integer or a rounded float)
    results = []
    for card in board_results:
        text = card.text
        if text != 'Inf':
            try:
                results.append(float(text))
            except ValueError:
                pytest.fail(f"Card text '{text}' is not a valid number")

def test_center_cards_horizontally():
    cards = create_board_operations()
    initial_x_positions = [card.rect.x for card in cards]
    start_x = 50

    center_cards_horizontally(cards, start_x)

    # Check that each card's x position is incremented by start_x
    for card, initial_x in zip(cards, initial_x_positions):
        assert card.rect.x == initial_x + start_x