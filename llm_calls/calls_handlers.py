from llm_calls.config import Config
import os
import instructor
import pandas as pd
from anthropic import Anthropic
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv, find_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

api_key = Config.anthropic_api_key


class JobDescriptionKeywords(BaseModel):
    """Structured extraction of filtering keywords from a job description"""

    primary_keywords: List[str] = Field(
        ...,
        description="Core terms that directly identify the job's module, function, area, focus, or level. These are high-confidence matches to taxonomy terms (e.g., 'Asset Management', 'Client Service', 'Senior')",
        min_length=1
    )

    secondary_keywords: List[str] = Field(
        default_factory=list,
        description="Supporting terms and synonyms that provide additional context or alternative terminology for filtering (e.g., 'broker support', 'administrative', 'problem resolution')"
    )


def extract_job_keywords(job_description: str) -> JobDescriptionKeywords:
    """Extract filtering keywords from a job description"""

    client = instructor.from_anthropic(Anthropic(api_key=api_key))

    system_prompt = Config.keyword_prompt

    message = client.messages.create(
        model=Config.haiku_model,
        max_tokens=1500,
        system=system_prompt,
        messages=[
            {"role": "user", "content": job_description}
        ],
        response_model=JobDescriptionKeywords
    )
    json_response = message.model_dump(by_alias=True)
    return json_response


class JobMatchResults(BaseModel):
    """Top matching job codes from the taxonomy table"""

    top_job_codes: List[str] = Field(
        ...,
        description="List of 5 job codes from the filtered dataframe that best match the job description, ordered from best to worst match (e.g., ['BR.MAMF.F1', 'CH.MAMF.F1', ...])",
        min_length=5,
        max_length=5
    )

    reasoning: str = Field(
        ...,
        description="Brief explanation of why these top 5 job codes were selected and how they match the job description"
    )


def select_top_job_matches(
        job_description: str,
        filtered_df: pd.DataFrame
) -> JobMatchResults:
    """Select top 5 matching job codes from filtered dataframe"""

    client = instructor.from_anthropic(Anthropic(api_key=api_key))

    # Convert dataframe to structured text for the LLM
    df_context = "Here is the filtered candidate dataframe:\n\n"
    for idx, row in filtered_df.iterrows():
        df_context += f"Row {idx + 1}:\n"
        df_context += f"  Job Code: {row['Job Code']}\n"
        df_context += f"  Job Title: {row['Job Title']}\n"
        df_context += f"  Job Function: {row['Job Function']}\n"
        df_context += f"  Job Area: {row['Job Area']}\n"
        df_context += f"  Job Focus: {row['Job Focus']}\n"
        df_context += f"  Job Level: {row['Job Level']}\n"
        df_context += f"  Function Definition: {row['Function Definition']}\n"
        df_context += f"  Detailed Definition: {row['Detailed Definition'][:200]}...\n"
        df_context += "\n"

    user_message = f"""Job Description:
{job_description}

{df_context}

Please analyze this job description against the filtered candidates and return the top 5 best matching job codes."""

    system_prompt = Config.finder_prompt  # Store the XML prompt in your Config

    message = client.messages.create(
        model=Config.sonnet_model,  # Use Sonnet for better reasoning
        max_tokens=2000,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message}
        ],
        response_model=JobMatchResults
    )

    return message


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

    # Test the extraction
    result = extract_job_keywords(job_description)

    print("Primary Keywords:", result["primary_keywords"])
    print("\nSecondary Keywords:", result["secondary_keywords"])