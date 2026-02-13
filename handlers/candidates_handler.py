from find_candidates.excel_handler import ExcelHandler
from llm_calls.calls import extract_job_keywords, select_top_job_matches
import anthropic
from  dotenv import load_dotenv

load_dotenv()

def count_tokens(text: str, model: str = "claude-sonnet-4-20250514") -> int:
    """
    Count the number of tokens in a text string for a given Claude model.

    Args:
        text: The input text to count tokens for
        model: The Claude model name (default: claude-sonnet-4-20250514)

    Returns:
        The number of tokens in the text
    """
    client = anthropic.Anthropic()

    token_count = client.messages.count_tokens(
        model=model,
        messages=[{"role": "user", "content": text}]
    )

    return token_count.input_tokens
class Finder:

    def __init__(self, job_description: str):
        self.job_description = job_description
        self.excel_handler = ExcelHandler('../data/2025_Radford_job_structure_and_descriptions.xlsx')
        self.df = self.excel_handler.read_file()

    def get_rows_from_keywords(self):
        keywords = extract_job_keywords(self.job_description)
        primary = keywords["primary_keywords"]
        secondary = keywords["secondary_keywords"]
        primary_filter = self.excel_handler.filter_rows_by_strings(primary)
        if count_tokens(primary_filter.to_string()) <= 50000:
            return primary_filter
        else:
            secondary_filter = self.excel_handler.filter_rows_by_strings(secondary)
            return secondary_filter

    def get_top_5_candidates(self):
        final_df = self.get_rows_from_keywords()
        top_5 = select_top_job_matches(self.job_description, final_df)
        return top_5.model_dump()

if __name__ == '__main__':
    job_description = """
        Senior Data Scientist - Investment Analytics

        We are seeking an experienced Data Scientist to join our Asset Management team. You will develop and deploy machine learning models to support portfolio management decisions and enhance our quantitative investment strategies.

        Key Responsibilities:
        - Build predictive models for asset allocation and risk assessment
        - Develop algorithms for market trend analysis and alpha generation
        - Work with portfolio managers to translate investment hypotheses into data-driven solutions
        - Create data pipelines and automation tools for research workflows
        - Collaborate with quantitative researchers on factor modeling and backtesting frameworks
        - Present analytical findings and model performance to senior leadership

        Requirements:
        - 5+ years of experience in data science, preferably in financial services
        - Strong proficiency in Python (pandas, scikit-learn, TensorFlow) and SQL
        - Deep understanding of statistical modeling and machine learning techniques
        - Knowledge of financial markets, particularly equity and fixed income products
        - Experience with cloud platforms (AWS/Azure) and big data technologies
        - PhD or Master's degree in Statistics, Computer Science, Mathematics, or related quantitative field

        This role requires someone who can bridge the gap between data science and investment management, working across multiple asset classes to deliver actionable insights.
        """
    finder = Finder(job_description)
    print(finder.get_top_5_candidates())





