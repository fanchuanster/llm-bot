from vllm import LLM

# mistralai/Mistral-7B-Instruct-v0.3
llm = LLM("mistralai/Mistral-7B-Instruct-v0.3")

input = """Below, between <REF> and </REF>, is the content of a resolved ticket, which may include interactions between the submitter and agents.
<REF>[Metadata]:
id: IM00485201
company: MUFG UNION BANK NA
title: Monthly Report is not Generated for March
open_time: 03/01/2024 10:26
close_time: 03/01/2024 11:39
assignee_name: thanh.phan
priority: 2 (High)
severity: 2 (High)
impact: 3 - Multiple Users
assignment: SaaS ALM QC Consulting
resolution_code: Functionality Restored
status: closed 
[Content]:
03/01/2024 10:26
URL: https://almmufgunionbank.saas.microfocus.com/qcbin/there is a monthly database job that genetateing reports at first day of months. but the 03/01/2024, the report s have not fully generated. (see attached file). please check it for us.
03/01/2024 10:28
&#06;User updated ticket details.
-------------------------------------------------------------------------

03/01/2024 10:57
The job has been corrected to uploaded all 5 files.
-------------------------------------------------------------------------

03/01/2024 10:58
Corrected Jenkins job to send  out all 5 files.

Ticket Resolved
-------------------------------------------------------------------------

03/01/2024 11:39
Ticket has been Closed
-------------------------------------------------------------------------
</REF>
You, as an OpenText support engineer, please perform the following tasks:
1. Extract a detailed summary of the reported issue, including the original error message if available.
2. If solution is available in the ticket, extract it with detailed instructions.
3. Determine whether the extracted content (issue summary and solution) should be saved into the knowledge base for future reference.
4. Provide your response strictly conforming to the following JSON format:
Please respond STRICTLY conforming to the following JSON format:
{
    "Issue": "<detailed summary>", 
    "Solution": "<detailed solution>", 
    "Save to Knowledge Base": "<yes or no>",
    "Why Save to Knowledge Base": "<explanation>"
}"""
print(llm.generate(input))