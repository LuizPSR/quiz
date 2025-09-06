import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


# assignment unit tests

def test_create_question_with_max_title_length():
    question = Question('a'*100)
    assert question.id != None

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question('q1', points = -1)
    with pytest.raises(Exception):
        Question('q2', points = 0.95)
    with pytest.raises(Exception):
        Question('q3', points = 101)

def test_create_multiple_choices():
    q1 = Question('q1')
    a = q1.add_choice('a')
    b = q1.add_choice('b')
    c = q1.add_choice('c')
    assert len(q1.choices) == 3

def test_remove_choice_by_id():
    q1 = Question('q1')
    a = q1.add_choice('a')
    b = q1.add_choice('b')
    c = q1.add_choice('c')

    q1.remove_choice_by_id(b.id)
    assert b not in q1.choices

def test_remove_all_choices():
    q1 = Question('q1')
    a = q1.add_choice('a')
    b = q1.add_choice('b')
    c = q1.add_choice('c')

    q1.remove_all_choices()
    assert len(q1.choices) == 0

def test_remove_invalid_id():
    q1 = Question('q1')
    a = q1.add_choice('a')
    with pytest.raises(Exception):
        q1.remove_choice_by_id(a.id+1)

def test_setting_correct_choice():
    q1 = Question('q1')
    a = q1.add_choice('a')
    b = q1.add_choice('b')
    c = q1.add_choice('c')

    q1.set_correct_choices([b.id])
    assert b.is_correct == True

def test_setting_correct_invalid_choice():
    q1 = Question('q1')
    a = q1.add_choice('a')
    with pytest.raises(Exception):
        q1.set_correct_choices(a.id+1)

def test_correcting_selection():
    q1 = Question('q1')
    a = q1.add_choice('a', True)
    b = q1.add_choice('b')
    c = q1.add_choice('c')

    answer = q1.correct_selected_choices([a.id])
    assert len(answer) == 1

    answer = q1.correct_selected_choices([b.id])
    assert len(answer) == 0

def test_valid_multiple_selection():
    q1 = Question('q1', max_selections=2)
    a = q1.add_choice('a', True)
    b = q1.add_choice('b')
    c = q1.add_choice('c')

    answer = q1.correct_selected_choices([a.id, b.id])
    assert len(answer) == 1

    answer = q1.correct_selected_choices([b.id])
    assert len(answer) == 0

# I run out of ideas for the fixture, so a moved one of the regular test to it and made more unit tests

@pytest.fixture
def example_question():
    q1 = Question('q1', max_selections=2)
    a = q1.add_choice('a', True)
    b = q1.add_choice('b')
    c = q1.add_choice('c')
    d = q1.add_choice('d', True)
    return q1

def test_correcting_invalid_ids(example_question):
    # should ignore as if wrong
    answer = example_question.correct_selected_choices([example_question.choices[-1].id+1])
    assert len(answer) == 0

def test_too_many_selections(example_question):
    with pytest.raises(Exception):
        q1.correct_selected_choices([1, 2, 3])