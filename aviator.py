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
prompt = """ Below is the detailed description of a ticket, which may include interactions between the submitter and agents:
Ticket Metadata:
Status: updated
Open_time: 2024-04-05T06:37:56-07:00
Priority: 2 (High)
Assignment: SaaS ALM PC Production
Resolution_code: 
Severity: 1 (Very High)
Impact: 4 - Single User
Id: IM00486182
Company: 3M COMPANY
Title: Failed to Collate Results
Close_time: 
Assignee: daniela.gomez
This is happening 2nd time with LRE SaaS. Following tests has failed to collate the results.
 
Run ID:
17213
17214
17215
 
It will be helpful if you can recover the results from above runs. 
 
Thank You!
The other 2 tickets for RUNIDS

IM00486187 - RUNID 17214

IM00486188 - RUN ID 17215
- - -

&#06;All the runs could be found from: 
Domain: SAP
Project: Polaris
- - -

RUN 17213

Domain: SAP

Project: Polaris

Controller LREORG025P-C5
	
IP 10.210.10.153

LG lgprodsvr58.mmm.com(80);
lgprodsvr52.mmm.com(69);
lgprodsvr78.mmm.com(58);
lgprodsvr53.mmm.com(100);
lgprodsvr55.mmm.com(43);
lgprodsvr54.mmm.com(74);
lgprodsvr87.mmm.com(39);
lgprodsvr90.mmm.com(110);
lgprodsvr83.mmm.com(39);
lgprodsvr82.mmm.com(39);
lgprodsvr81.mmm.com(40);
lgprodsvr89.mmm.com(112);
lgprodsvr57.mmm.com(40);
lgprodsvr56.mmm.com(75);
lgprodsvr85.mmm.com(39)

https://lremmm.saas.microfocus.com/LRE/?tenant=1dbe834a-7489-47af-a488-bdfdc45ed841

SSO URLs:

Admin:
https://lremmm.saas.microfocus.com/admin/adminx/login?tenant=1dbe834a-7489-47af-a488-bdfdc45ed841&saas-auth=internal

Projects:
https://lremmm.saas.microfocus.com//Loadtest/pcx/app/dashboard?tenant=1dbe834a-7489-47af-a488-bdfdc45ed841&saas-auth=internal
- - -

Collation completed, files uploaded, No Vusers LOGs folder for this RUN.
- - -

Hello Ajay,

We are following up on the request SD00477942

We have manually collated the results for RUN ID 17213

Please check and confirm.

Regards,
Leonardo Salazar
Open text Software-as-a-Service
Toll Free: +1 855 525 9252
&#06;Thanks! I can see the results now. But why did this happen as its happening 2nd time. I noticed all the 3 runs kept running for over 23hrs, whereas test was designed to run only for about 6.5hrs. So question is why the Controller failed to force stop the test at 6.5hrs. In past I created ticket SD00475879 for exact same issue. It would be great if you can help find a permanent fix for this issue just so it doesn't happen in future tests. Appreciate your support!
- - -

Hello team can you help to check why this test lasted more than 23 hours instead of the 6 hours configure?

*******Bosco confirmed this can be send to LRE queue*******

After checking the EVENT LOG for RUN ID 17213 I can see the test was expected to run for around 6 hours and ran for +23 hours.

Checking the event LOG I see an event that lasted around 16 hours, from April 4th 3 pm, until April 5th 7 am
(check attachment Event LOG run ID17213.JPG)

More details:

RUN ID 17213

Domain: SAP
Project: Polaris

Controller LREORG025P-C5
	
IP 10.210.10.153

Up time 17 days

SSO URLs:

Admin:

https://lremmm.saas.microfocus.com/admin/adminx/login?tenant=1dbe834a-7489-47af-a488-bdfdc45ed841&saas-auth=internal

Projects:

https://lremmm.saas.microfocus.com//Loadtest/pcx/app/dashboard?tenant=1dbe834a-7489-47af-a488-bdfdc45ed841&saas-auth=internal
- - -

Hello Ajay,

I'm Daniela Gomez from SaaS Delivery team, I'll be assisting you on this case.

Let me review your case and I'll update you soon

Regards
Daniela Gomez
Lead Cloud Applications Engineer
- - -

checking
- - -

.
- - -

wip
- - -

Last Update SLO Breached - 2 00:00:17 Hrs passed. Assignee: daniela.gomez
Greetings,

I want to let you know that I'm still working on your case.

As soon as I have an update I'll let you know.
Regards,
- - -

.
- - -

Last Update SLO Breached - 2 00:00:21 Hrs passed. Assignee: daniela.gomez
cheking.
- - -

.
- - -

wip
- - -

.
- - -

wip
- - -

.
- - -

.
- - -

.
- - -

wip
- - -

.
- - -

.
- - -

.
- - -

.
- - -

.
- - -

Greetings,
An update will be providing soon.
Regards
- - -

Please provide a technical summary of the ticket for review progress and status. Also, rigorously evaluate the customer sentiment score, customer satisfaction score, and agent service quality score, on a scale of 1-10, based on the ticket handling process regardless of the impact and severity of the issue reported or experienced, to enable the manager to identify cases of low satisfaction early and take proactive intervention. 
	Then evaluate the Criticality Score on a 1 (least-critical) - 10 (most-critical) scale by the ticket Metadata \"Impact\", \"Severity\" and \"Priority\" and the context. Finally, suggest necessary follow-up actions. Expected output: 
	- Technical Summary: 
	- Customer Sentiment Score: 
	- Customer Satisfaction Score: 
	- Service Quality Score: 
	- Criticality Score:
	- Follow-up Actions:
	If insufficient context details are available, assume a high score. Only evaluate based on the facts happened but not guessing or assumption for the future
2024/06/23 09:11:07 ====================== Result ====================
2024/06/23 09:11:07 IM00486182:  Technical Summary: The ticket is related to a load testing issue where the controller failed to force stop the test after 6.5 hours, resulting in the test running for over 23 hours. The assignee, Daniela Gomez, is investigating the issue and checking the event log for more information.
Customer Sentiment Score: 7 (Neutral)
The customer seems to be frustrated with the length of time the test took, but they also acknowledge that the issue has been raised before and there might be a permanent fix needed. They appreciate the support received so far.

Customer Satisfaction Score: 6 (Fairly Unsatisfied)
While the customer is satisfied with the initial response and acknowledgment of their query, they are unhappy with the duration of the test and the fact that it exceeded the configured time limit.

Service Quality Score: 8 (Good)
The agent responded promptly and provided clear updates throughout the conversation. However, the issue itself is causing dissatisfaction.

Criticality Score: 8 (High)
Based on the Impact, Severity, and Priority metadata, this ticket is considered highly critical. The test failure caused significant delays and affected the overall performance of the system.
Follow-up Actions:

1. Escalate the issue to the appropriate teams for further investigation and resolution.
2. Provide regular updates to the customer until the issue is resolved.
3. Review the Load Test configuration and ensure that it is set up correctly to prevent similar issues in the future.
2024/06/23 09:11:07 Progress 2/320 - IM00488596
2024/06/23 09:11:14 ====================== Prompt ====================
2024/06/23 09:11:14 Below is the detailed description of a ticket, which may include interactions between the submitter and agents:
Ticket Metadata:
Priority: 3 (Medium)
Assignment: Frontline
Company: ACCENTURE PEOPLESOFT TEAM
Close_time: 
Assignee: Hamsa.Selvarajan
Impact: 4 - Single User
Resolution_code: 
Status: updated
Id: IM00488596
Title: Cannot login to VuGen - LoadRunner Cloud Integration
Open_time: 2024-06-18T20:45:10-07:00
Severity: 2 (High)
hen trying to Login/Aunthenticate via VuGen
Following error shows
 
 
Authentication failed with error: Post https://loadrunner-cloud.saas.microfocus.com/v1/auth?TENANTID=918843891: read tcp 10.18.161.22:6088->52.89.63.41:443: wsarecv: An existing connection was forcibly closed by the remote host.
Please provide a technical summary of the ticket for review progress and status. Also, rigorously evaluate the customer sentiment score, customer satisfaction score, and agent service quality score, on a scale of 1-10, based on the ticket handling process regardless of the impact and severity of the issue reported or experienced, to enable the manager to identify cases of low satisfaction early and take proactive intervention. 
	Then evaluate the Criticality Score on a 1 (least-critical) - 10 (most-critical) scale by the ticket Metadata \"Impact\", \"Severity\" and \"Priority\" and the context. Finally, suggest necessary follow-up actions. Expected output: 
	- Technical Summary: 
	- Customer Sentiment Score: 
	- Customer Satisfaction Score: 
	- Service Quality Score: 
	- Criticality Score:
	- Follow-up Actions:
	If insufficient context details are available, assume a high score. Only evaluate based on the facts happened but not guessing or assumption for the future
2024/06/23 09:11:14 ====================== Result ====================
2024/06/23 09:11:14 IM00488596:  Technical Summary: The user is unable to log in to VuGen due to an authentication failure with the error message "Post https://loadrunner-cloud.saas.microfocus.com/v1/auth?TENANTID=918843891: read tcp 10.18.161.22:6088->52.89.63.41:443: wsarecv: An existing connection was forcibly closed by the remote host.".
Customer Sentiment Score: 8/10
The customer's sentiment can be inferred from their use of strong language such as "cannot login" and "error message". However, there is no indication of frustration or anger, suggesting that the customer's emotional state is neutral rather than negative.
Customer Satisfaction Score: 6/10
Based on the information provided, it seems unlikely that the customer is satisfied with the current level of support they are receiving. The lack of success in resolving the issue after multiple attempts suggests that the customer's expectations have not been met.
Service Quality Score: 7/10
While the agent has responded promptly and provided some troubleshooting steps, the resolution of the issue remains elusive. This could indicate a gap in the service quality delivered by the agent.
Criticality Score: 9/10
Given the high priority assigned to this ticket and the severe impact on the customer's ability to access VuGen, the criticality score is relatively high.
Follow-up Actions:
* Escalate the ticket to a higher-level engineer for further investigation and resolution.
* Provide
2024/06/23 09:11:14 Progress 3/320 - IM00488097
2024/06/23 09:11:22 ====================== Prompt ====================
2024/06/23 09:11:22 Below is the detailed description of a ticket, which may include interactions between the submitter and agents:
Ticket Metadata:
Open_time: 2024-05-31T07:47:59-07:00
Close_time: 
Severity: 3 (Medium)
Impact: 4 - Single User
Resolution_code: 
Id: IM00488097
Company: ACCENTURE_ALM
Title: Change Date format in Defect Business Reports as per Client Request
Assignee: jose.vargas
Priority: 3 (Medium)
Assignment: Frontline
Status: updated
Change Date format from DD-MMM-YY to MM-DD-YY in the Business Graph/Report to be able to automatically sort the dates by default. This is a request from Client.
to me-.
- - -

Hi Mark,

Thank you for contacting Open Text.

Could you please provide us with the following information for us to be able to give you a better support.

ALM URL
Domain and Project name
Availability with working hours
Contact Information

Regards,
Jose Vargas
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
&#06;ALM URL: https://almaccentureprod.saas.microfocus.com/qcbin/
Domain: ASMPT
Project name: ASMPT 
Availability with working hours: 9AM to 7PM SGT
Contact Information: email via mark.jason.bongalos@accenture.com
- - -

ALM version 17.01
Patch Level 0
- - -

Hi Mark,

Following the issue in Support Case SD00480873, please review the information below:

Due to the nature of your request, we have opened the case 02887562 with Open Text Software Support on your behalf.

They will be contacting you via email.

Regards,
Jose Vargas
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Update from GSD to SaaS.
----------------------------------
Hello Saas team,

Thank you for contacting Opentext Support Customer.
My name is Fabian Esquivel from the QC/ALM Support Team and I will assist you with your case

The reason why i'm contacting you first that customer it is that actual date time by default come from the server.

please find note provided by R&D directly

\"Date format in project report is based on ALM server locale setting which is different from the ALM client UI. ALM client UI is based on the client OS setting.\"

Could you please review if the server is using that format and let me know it.

I'll be pending.
----------------------------
- - -

Hello Mark,

Our Software Support Team has now assigned an Engineer Fabian Esquivel, you should see an email from him email subject:

“02887562-SaaS Customer ACCENTURE_ALM SD00480873 Change Date format in Defect Business Reports as per Client Request”

The case has been updated with the following:

Hello Josue,

This is in the application server.

it will be depending if it is Windows or Linux,

for example in Linux, you can review this by going to Windows, settings. date and time. time format,

ALM will user the server time setting present in the client UI. this is a change that can't be done in the application directly and will affect the entire system,

Since it is saas it is not recommended to change this due this changes affect all users.



This will be something that has to be discussed internal with saas.

Please let me know how would you like to proceed.

Regards.
*****End of Software Support Email Communication

Take into consideration that our Software Support Team will continue communication through case 02887562.

Please check your inbox for any new emails and remember you can always reply directly to our Software Support team, they will be waiting for your response.


Thank you,

Hellen Mata
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hello Mark,

We would like to know if you received our previous communication?

Thank you,
Eduardo Flores
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
- - -

Hi Mark,

We would like to know if you could check our previous communication?

This change will be affecting the entire instance including all the existing projects the customer has at the moment, with this being said, would you like us to consult our production team to see if this is change can be done?

Regards,
Jose Vargas
OpenText Software-as-a-Service
Toll Free: +1 855 525 9252
Message from GSD to us.
---------------------------------
Hello Saas team,

I hope you are doing great.

We haven’t hear back from customer, I would like to know base on the configuration is directly in the saas server I would like to request the closure of the case. If a problem come making this change or have additional dobuts. You can reach me our directly.

Please let us know if it is ok for us to proceed.

Thanks for your comprehension
---------------------------------------------
We will re-open the case if needed.
- - -

Please provide a technical summary of the ticket for review progress and status. Also, rigorously evaluate the customer sentiment score, customer satisfaction score, and agent service quality score, on a scale of 1-10, based on the ticket handling process regardless of the impact and severity of the issue reported or experienced, to enable the manager to identify cases of low satisfaction early and take proactive intervention. 
	Then evaluate the Criticality Score on a 1 (least-critical) - 10 (most-critical) scale by the ticket Metadata \"Impact\", \"Severity\" and \"Priority\" and the context. Finally, suggest necessary follow-up actions. Expected output: 
	- Technical Summary: 
	- Customer Sentiment Score: 
	- Customer Satisfaction Score: 
	- Service Quality Score: 
	- Criticality Score:
	- Follow-up Actions:
	If insufficient context details are available, assume a high score. Only evaluate based on the facts happened but not guessing or assumption for the future"""
result = llama_model(prompt=prompt, max_new_tokens=5000)
print("Generated Text:", result)
