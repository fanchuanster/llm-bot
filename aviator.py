from langchain.llms.base import LLM
from typing import Optional, List
from langchain.prompts import PromptTemplate

class CustomLlamaLLM(LLM):

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        import requests
        # headers = {"Authorization": f"Bearer {self.api_key}"}
        headers = {
            # "Authorization": f"Basic {base64.b64encode(cred.encode()).decode()}",
            'Content-Type': 'application/json',
            # 'Accept': "application/json"
            }
        response = requests.post(
            f"http://10.210.34.38:8080/generate", 
            json={"inputs": prompt, "parameters": {"max_new_tokens": kwargs.get("max_new_tokens", 5000)}},
            headers=headers
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data["generated_text"]

    @property
    def _llm_type(self) -> str:
        return "custom_llama_llm"

# Usage example
# api_url = "http://10.210.34.38:8080"
# api_key = "your_api_key_here"
llama_model = CustomLlamaLLM()
prompt = """Below in between the <REF> and </REF> is the content of a ticket, which may include interactions between the submitter and agents. Please hold off responding until all the content is submitted which may be multiple submissions.
	<REF>
Ticket Metadata:
Company: ALLFUNDS BANK SA
Open_time: 2024-06-10T23:34:03-07:00
Close_time: 
Assignee: ajay.s
Impact: 3 - Multiple Users
Assignment: Frontline
Status: updated
Id: IM00488350
Title: Problem when running API type tests unattended
Priority: 2 (High)
Severity: 2 (High)
Resolution_code: 
When executing a test set of automatic API type tests from the automatic runner, sometimes, randomly, since it does not follow any pattern that we have been able to locate, the ALM automatic runner application gives the following error messages in some tests when launch the execution. This problem happens to us in all projects and with different users.
The error messages that we have been able to review that it returns are:
 
\"The connection to the specified ALM server failed\"
\"Remote procedure call error, RCP Server unavailable\"
 
We attach in the document some evidence of the problem of the tests that we have carried out both from ALM and from Jenkins.
Hello SOC Team,

Kindly check on this request and advise. Thanks!
- - -

Dear team,

Please involve the GSD team on this case.

If they need delivery help , you might contact us.

Thank you,
Georgi Georgiev

OpenText SaaS Team
- - -

&#06;Hello Team,
We indicate the requested information
Software version - UFT2022
OS System - Windows server 2016 / windows 10
Contact Person- Zeus Algaba / Rafael Garzón
Email ID - zeus.algaba@inetum.com / rafael.garzon@allfunds.com
Phone number - NA (teams meeting)
Time Zone - GMT+2
Working hours - 08:00 - 17:00 
Is it reproducible (Y/N)? Y
Steps to reproduce:
	1. open ALM :https://almallfundsbank.saas.microfocus.com/qcbin/
	2. Enter the project “AFAPP_86_APPIAN”
	3. Go to the test lab module
	4. Go to the test set “TESTSET_OPEN_TEXT_APIS_PROBLEM” located in
 		/Root/ AFAPP_86_APPIAN/functional/PRE/Appian/PRE/ 
	5. Click on “run test set”
	6. Click on the run all button on the pop-up screen.
	7. Wait for the test results (takes 10 mins max)
Affecting all users (Y/N)? Y
Summary of troubleshooting steps performed: Some of the tests executed randomly give the messages reported in the incident summary.
Thank you,
- - -

&#06;Additionally we include the ALM server version
 
ALM_HELP.PNG was attached.
- - -

Hello Team,

Following the issue in Support Case SD00481350 please review the information below:

Due to the nature of your request, we have opened case 02894927 with Micro Focus Software Support  on your behalf and have asked them to contact you directly.

This Support Request is currently marked Pending Vendor.

Thank you,	
S Ajay Kumar
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello,

Please find the below update from software support team.
- - ---------------------------------

Hello Team,

Thank you for contacting OpenText.

My name is Emmanuel from EMEA ALM/Octane Support Team.

Regarding the error in your environment, this seems that there is a communication issue into both applications; please follow these steps below:
•	Close UFT.
•	Opened IE as administrator (right-click IE > Run as Administrator) and navigated to ALM Tools.
•	From the ALM Tools page, selected \"ALM Connectivity\" and download/run on the affected client machine.
•	You should receive an \"Installation Successful\" message. From the ALM Tools page
•	Selected \"ALM Client Registration\" and \"Register ALM.\"
•	Log into your ALM Client to make sure that works.
•	Run UFT as administrator
•	Could now log into ALM from UFT and run UFT tests from ALM

SUMMARY
Please try to uninstall the ALM Client.
Re-register the client - http://<servername>:8080/qcbin/addins.html
Download HP ALM Connectivity Add in - http://<servername>:8080/qcbin/addins.html

In UFT:
Please make sure ALM connectivity is selected during configuration
Launch the UFT Client and see if you can connect to ALM and perform Test.

Expecting your feedback.

- - ---------------------------------

Thank you,
Shoney Thomas
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

&#06;Good afternoon,
 
We have carried out the indicated steps and we have carried out several tests, and the result has been KO, since we reproduced the problem (some tests give the result \"failed condition, because not executing any of the functionalities impacts not being able to execute the next one. ) 
 
As you can see in different executions, different tests are the ones that present problems when executing them.
 
We attach the evidence and are waiting for next steps.
 
Thank you so much,
Regards!
 
Evidences SD00481350.docx was attached.
- - -

Hello Team,

Thank you for the update. We have forwarded your recent mail to our support team. They would check and update you soon.

Thank you,
S Ajay Kumar
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

&#06;Good morning,
 
Our availability is from 08:00 -15:00 GMT+2.
 
They are not very large tests, and it also passes in several different tests and we have not detected that the size of the test could be a reason for what is happening.
 
We attach a screenshot of the agent of one of the test execution machines.
 
Thank you so much,
Regards!
 
AgentConfig.docx was attached.
- - -

Hello Team,

We have conveyed your recent mail to our support team. They would investigate further and provide you the updates.

Thank you,
S Ajay Kumar
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

&#06;Good afternoon,
 
We attach the requested information, we have carried out the exercise and the numerous logs with the timestamp that the tool automatically generates, in those logs there are two or three tests that have gone well and one that has given the reported problem.
 
Thank you so much,
Regards,
 
LogsApis.zip was attached.
- - -

Hi Zeus,

Thanks for the update. We have shared the attached file with the support team and will keep you posted once we recive an update.

Thank you,
Smitha Madhavan
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello,

We are looking forward to your response, Kindly keep us posted on the status from your end.


Thank you,
Hamsa Selvaraj
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello,

Please find the below update from software support team
- - ----------------------

Hello @Algaba-Porras Zeus,

1. Please can you confirm what is your UFT version?

2.  Also about this error- The connection to the specified ALM server failed
If you open UFT and connect to ALM from there- will it always connect without issues if you try few times?

However, if the UFT hosts are also on @MFI-SaaS Tier1 Support servers, we could check them directly (I am not sure if that is the case here).

3.  At the same time- can we have a meeting with @MFI-SaaS Tier1 Support team/engineer to test the below steps? Since you told us exactly how to reproduce it, can we get some logs and decide what to do next.

We would do this- (+ some logs gathering)
>> open ALM :https://almallfundsbank.saas.microfocus.com/qcbin/
>> Enter the project “AFAPP_86_APPIAN”
>> Go to the test lab module
>> Go to the test set “TESTSET_OPEN_TEXT_APIS_PROBLEM” located in /Root/ AFAPP_86_APPIAN/functional/PRE/Appian/PRE/
>> Click on “run test set”
>> Click on the run all button on the pop-up screen.
>> Wait for the test results and the error pops out.

Expecting update from the @MFI-SaaS Tier1 Support @Smitha Madhavan team for a meeting.

- - -------------------------------------------

Thank you,
Shoney Thomas
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello,

Please be informed on the recent update from the Software support team and let us know the required UFT version details to progress on this case.

Thank you,
Hamsa Selvaraj
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

&#06;Good morning, 
 
1.	Our UFT version is Version 2022 build 1004
 
2.	Yes, we haven’t problems with ALM connection from UFT
 
Thanks
- - -

Please hold off for more information.../nContinue
Hello,

Thanks for the update. We have informed the support team on the same and will keep you posted on the updates shortly.

Thank you,
Smitha Madhavan
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello,

Our software support team is handling this case internally.

We will update you as soon as we receive more information.

Thank you,
Doji John
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello Alejandro,

Thank you for confirming the availability. The same has been updated to software support team.

Thank you,
Shoney Thomas
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hi Alejandro,

We have followed up with Software support team to provide you with new updates,  Kindly look forward to the email from the team.

Thank you,
Hamsa Selvaraj
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

&#06;Hello, 
 
I attach the logs of the tests, it failed shortly after finishing the meeting as well as some screenshots of the moment of the error. If any file is missing, please tell me which one. 
Thanks
 
LOGS.zip was attached.
ErrorALM.png was attached.
Scheduler_2406_121244.log was attached.
- - -

Hello,

Thank you for attaching the logs. The same information has been shared to software support team.

Thank you,
Shoney Thomas
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello

Our Software Support team is still working on the issue and will keep you posted with the updates once we hear from them.

 Thank you,
Madhu Bala M
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello Team,

We have discussed this with our internal team and got an update that

-  ALM have plenty of disk space
-  DB servers is fine
 - They safe-restarted the farm with the health checker enabled.

Our team suggested to try to run the tests again and let us know the outcome.

We will stay attentive to your comments.

Thank you,
S Ajay Kumar
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello Team,

Please be aware of the recent update from Software Support team.

Looking forward to your response.

Thank you,
Doji John
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
</REF>
Provide a technical summary of the ticket for progress and status review. Also, rigorously evaluate the Customer Sentiment Score, customer satisfaction score, and agent service quality score, on a scale of 1-10, regardless of the impact and severity of the issue reported, to enable the manager to identify cases of low satisfaction early and take proactive intervention. 
	Then evaluate the Criticality Score on a 1 (least) - 10 scale by the ticket Metadata "Impact", "Severity" and "Priority". Finally, suggest necessary follow-up actions. Please respond STRICTLY confirming to following JSON format without extraneous: 
	{"Technical Summary": "<summary>", "Customer Sentiment Score": <integer>, "Customer Satisfaction Score": <integer>, "Service Quality Score": <integer>, "Criticality Score": <integer>, "Follow-up Action": "<Actions>"}
	Evaluate only based on the facts provided. The scores fields should be inegers without explanation beside. Double check if it confirms to JSON format."""
result = llama_model(prompt=prompt, max_new_tokens=5000)
print("Generated Text:", result)
