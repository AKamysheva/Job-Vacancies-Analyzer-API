import pytest
from app.services.cover_letter import ResumeReader
from app.services.vacancy_service import clean_description, get_skills, filter_vacancies
from unittest.mock import patch


@pytest.fixture
def mock_pdf_page(mocker):
    page = mocker.Mock()
    return page


@pytest.fixture
def mock_pdf_file(mock_pdf_page, mocker):
    pdf_file = mocker.Mock()
    pdf_file.pages = [mock_pdf_page]
    pdf_file.__enter__ = mocker.Mock(return_value=pdf_file)
    pdf_file.__exit__ = mocker.Mock(return_value=None)
    return pdf_file


@pytest.fixture
def resume_reader(mock_pdf_file):
    with (
        patch("app.services.cover_letter.settings.RESUME_PATH", "resume.pdf"),
        patch("app.services.cover_letter.pdfplumber.open", return_value=mock_pdf_file),
    ):
        yield ResumeReader()


def test_read_text_with_only_text(mock_pdf_page, resume_reader):
    mock_pdf_page.extract_table.return_value = None
    mock_pdf_page.extract_text.return_value = "Just plain text."
    result = resume_reader.read_text()
    assert result == "Just plain text.\n"


def test_read_text_with_table_and_text(mock_pdf_page, resume_reader):
    mock_pdf_page.extract_table.return_value = [
        ["Name", "Email"],
        ["Test Name", "test@example.com"],
    ]
    mock_pdf_page.extract_text.return_value = "Test resume text."
    result = resume_reader.read_text()
    expected = "Name | Email\n" "Test Name | test@example.com\n" "Test resume text.\n"
    assert result == expected


test_cases = [
    ({"description": "<highlighttext>Test 1</highlighttext>"}, "Test 1"),
    ({"snippet": {"requirement": "<highlighttext>Test 2</highlighttext>"}}, "Test 2"),
    (
        {"snippet": {"responsibility": "<highlighttext>Test 3</highlighttext>"}},
        "Test 3",
    ),
    ({"description": "Test 4"}, "Test 4"),
    ({}, "Описание отсутствует"),
]


@pytest.mark.parametrize("input_item, expected", test_cases)
def test_clean_description(input_item, expected):
    assert clean_description(input_item) == expected


test_cases_2 = [
    ({"key_skills": [{"name": "Python"}, {"name": "Docker"}]}, ["Python", "Docker"]),
    (
        {"key_skills": [], "professional_roles": [{"name": "Backend Developer"}]},
        ["Backend Developer"],
    ),
    ({"professional_roles": [{"name": "Data Analyst"}]}, ["Data Analyst"]),
    ({}, []),
]


@pytest.mark.parametrize("input_item, expected", test_cases_2)
def test_get_skills(input_item, expected):
    assert get_skills(input_item) == expected


def test_filter_vacancies(fake_vacancies):
    filtered_vacancies = filter_vacancies(fake_vacancies, "Python")
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0]["hh_id"] == 567894
