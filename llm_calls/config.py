import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    anthropic_api_key: str = os.environ.get("ANTHROPIC_API_KEY")
    haiku_model = os.environ.get("HAIKU_MODEL")
    sonnet_model = os.environ.get("SONNET_MODEL")
    keyword_prompt: str = """
<task>
You are a job classification expert. Extract keywords from a job description that will filter against a structured job taxonomy table.
</task>

<taxonomy_reference>
You will match against a table with these columns:
Job Module, Job Code, Job Title, Job Function, Job Area, Job Focus, Job Level, Module Code, Function Code, Area Code, Focus Code, Level Code, Module Definition, Function Definition, Area Definition, Focus Definition, Detailed Definition

EXAMPLE ROWS:

Row 1:
- Job Module: Asset Management Sales
- Job Code: BR.MAMF.F1
- Job Title: Broker Dealer / Independent Agent Services - Multi-Area - Multi-Focus - Entry (F1)
- Job Function: Broker Dealer / Independent Agent Services
- Job Area: Multi-Area
- Job Focus: Multi-Focus
- Job Level: Entry (F1)
- Function Definition: Provides problem resolution, operations and administrative support to registered representatives and clients. Works with intermediaries who have purchased the organization's products.

Row 2:
- Job Module: Asset Management Sales
- Job Code: CH.MAMF.F1
- Job Title: Corporate Access - Multi-Area - Multi-Focus - Entry (F1)
- Job Function: Corporate Access
- Job Area: Multi-Area
- Job Focus: Multi-Focus
- Job Level: Entry (F1)
- Function Definition: Provides consultative and logistics services that introduce PMs and analysts to third-party information sources (corporate executives, expert networks, research services, alternative data).
</taxonomy_reference>

<instructions>
Extract two types of keywords:

**Primary Keywords** - Terms that directly match taxonomy categories:
- Job modules (e.g., "Asset Management", "Sales")
- Job functions (e.g., "Client Service", "Broker Dealer", "Corporate Access")
- Job areas (e.g., "Multi-Area", specific domains)
- Job focus (e.g., "Multi-Focus", specializations)
- Job levels (e.g., "Entry", "Senior", "Lead", "Executive")

**Secondary Keywords** - Supporting terms:
- Synonyms and variations
- Related activities and responsibilities
- Technical terms and qualifications
- Industry-specific terminology

<thinking>
Before extracting, reason through:
1. What is the core job role and function?
2. What business area/module does it belong to?
3. What level of seniority is indicated?
4. What specific or broad (multi-area/multi-focus) scope?
5. What related terms would help filter the taxonomy table?
</thinking>
</instructions>

<examples>
<example>
<job_description>
Junior Client Service Representative for broker inquiries about investment products. Provides administrative support and problem resolution for registered representatives.
</job_description>

<thinking>
- Core function: Client service supporting brokers
- Module: Investment products → Asset Management Sales
- Function: Matches "Broker Dealer / Independent Agent Services" (problem resolution, admin support, registered representatives)
- Level: "Junior" → Entry level
- Scope: No specific area mentioned → Multi-Area
- Related terms: administrative, support, inquiries
</thinking>

<output>
{
  "primary_keywords": [
    "Client Service",
    "Broker Dealer",
    "Asset Management",
    "Sales",
    "Entry",
    "Junior",
    "Multi-Area",
    "registered representatives"
  ],
  "secondary_keywords": [
    "administrative support",
    "problem resolution",
    "investment products",
    "broker inquiries",
    "customer service"
  ]
}
</output>
</example>
</examples>

<output_requirements>
Return a valid JSON object:
{
  "primary_keywords": ["term1", "term2", ...],
  "secondary_keywords": ["term1", "term2", ...]
}

- Include 5-15 primary keywords
- Include 3-10 secondary keywords
- Use exact terms from the job description when possible
- Include variations that match taxonomy terminology
</output_requirements>

Now, please provide the job description you want analyzed.
"""
    finder_prompt: str = """
    <task>
You are a job classification expert. Your task is to analyze a job description and select the top 5 best matching job codes from a filtered taxonomy table.
</task>

<context>
You will receive:
1. A job description (unstructured text describing a role)
2. A filtered dataframe with candidate job codes from the taxonomy table

The dataframe contains these columns:
- Job Module, Job Code, Job Title, Job Function, Job Area, Job Focus, Job Level
- Module Code, Function Code, Area Code, Focus Code, Level Code  
- Module Definition, Function Definition, Area Definition, Focus Definition, Detailed Definition
</context>

<instructions>
Analyze the job description against each row in the filtered dataframe and select the top 5 best matches.

<thinking>
Work through this reasoning process:

1. **Understand the job description**:
   - What is the primary function/responsibility?
   - What level of seniority is indicated?
   - What business area or module does it belong to?
   - What specific focus or specialization is mentioned?
   - What scope does it have (specific vs. multi-area/multi-focus)?

2. **Score each candidate**:
   - **Function match** (highest weight): Does the job function definition align with the description's responsibilities?
   - **Level match**: Does the level (Entry/Senior/Lead/Executive) match the seniority indicators?
   - **Area/Focus match**: Does the area and focus align with the specialization mentioned?
   - **Module match**: Is it in the right business area?
   - **Definition alignment**: Does the detailed definition capture the essence of the role?

3. **Handle ambiguity**:
   - If the job spans multiple areas, prioritize "Multi-Area" codes
   - If no specific focus is clear, prioritize "Multi-Focus" codes
   - If multiple candidates are equally good, prefer more specific over generic matches

4. **Rank and select**:
   - Order from best match to 5th best match
   - Ensure diversity in your selection if multiple similar codes exist
   - Return exactly 5 job codes

5. **Validate selection**:
   - Do all 5 codes make logical sense for this job description?
   - Is there a clear rationale for each selection?
   - Are they ordered correctly by match quality?
</thinking>

Return the top 5 job codes and a brief reasoning for your selections.
</instructions>

<matching_criteria>
**High Priority Matches:**
- Job function closely aligns with primary responsibilities
- Level matches seniority indicators (years of experience, leadership scope)
- Detailed definition captures the core essence of the role

**Medium Priority Matches:**
- Area and focus align with mentioned specializations
- Module matches the business context
- Job title has similar terminology

**Lower Priority Matches:**
- Generic definitions that could apply to many roles
- Partial matches on only 1-2 dimensions
- Codes that require significant interpretation to fit
</matching_criteria>

<examples>
<example>
<job_description>
Junior Client Service Representative for broker inquiries about investment products. Provides administrative support and problem resolution for registered representatives.
</job_description>

<filtered_dataframe>
Row 1: Job Code: BR.MAMF.F1, Job Function: Broker Dealer / Independent Agent Services, Job Level: Entry (F1), Function Definition: Provides problem resolution, operations and administrative support to registered representatives...

Row 2: Job Code: CH.MAMF.F1, Job Function: Corporate Access, Job Level: Entry (F1), Function Definition: Provides consultative and logistics services that introduce PMs and analysts to third-party information sources...

Row 3: Job Code: CS.MAMF.F1, Job Function: Client Service, Job Level: Entry (F1), Function Definition: Handles client inquiries and service requests...

Row 4: Job Code: BR.MAMF.F2, Job Function: Broker Dealer / Independent Agent Services, Job Level: Intermediate (F2), Function Definition: Provides problem resolution, operations and administrative support...

Row 5: Job Code: SA.MAMF.F1, Job Function: Sales Support, Job Level: Entry (F1), Function Definition: Provides administrative support to sales teams...

Row 6: Job Code: OP.MAMF.F1, Job Function: Operations Support, Job Level: Entry (F1), Function Definition: Handles operational tasks and administrative duties...
</filtered_dataframe>

<thinking>
1. Job description analysis:
   - Primary function: Client service for brokers, problem resolution, administrative support
   - Level: "Junior" → Entry level (F1)
   - Key terms: "broker inquiries", "registered representatives", "administrative support", "problem resolution"
   - This is clearly a support role for broker-dealers

2. Scoring candidates:
   - BR.MAMF.F1: EXCELLENT match - exact function (Broker Dealer services), exact level (F1), definition mentions "problem resolution" and "registered representatives"
   - CS.MAMF.F1: GOOD match - client service aligns, correct level, but less specific than BR
   - SA.MAMF.F1: MODERATE match - support role, correct level, but focused on sales not brokers
   - BR.MAMF.F2: GOOD match - correct function but wrong level (F2 vs F1)
   - OP.MAMF.F1: MODERATE match - operations/admin support fits, correct level, but less specific
   - CH.MAMF.F1: POOR match - Corporate Access is about connecting PMs to info sources, not broker support

3. Ranking:
   1. BR.MAMF.F1 - Perfect match on all dimensions
   2. CS.MAMF.F1 - Strong function match, correct level
   3. SA.MAMF.F1 - Support role with correct level
   4. BR.MAMF.F2 - Correct function but elevated level
   5. OP.MAMF.F1 - Generic support role that fits
</thinking>

<output>
{
  "top_job_codes": [
    "BR.MAMF.F1",
    "CS.MAMF.F1", 
    "SA.MAMF.F1",
    "BR.MAMF.F2",
    "OP.MAMF.F1"
  ],
  "reasoning": "BR.MAMF.F1 is the best match as it specifically covers broker dealer services with problem resolution and support for registered representatives at entry level. CS.MAMF.F1 is second as it captures the client service aspect. SA.MAMF.F1 and OP.MAMF.F1 provide fallback options for general support roles. BR.MAMF.F2 is included as a near-match with correct function but intermediate level."
}
</output>
</example>
</examples>

<output_requirements>
- Return exactly 5 job codes in order of best to worst match
- Job codes must exist in the filtered dataframe provided
- Provide clear reasoning for the selection
- Ensure ordering reflects match quality (best first, 5th best last)
</output_requirements>

<quality_criteria>
- Top match should align on function, level, and area/focus
- Include the most specific matches available
- Avoid redundant codes unless they represent meaningful alternatives
- Consider the complete detailed definition, not just job titles
- If fewer than 5 good matches exist, still return 5 ordered by quality
</quality_criteria>
    """