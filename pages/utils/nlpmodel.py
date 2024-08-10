from openai import OpenAI

class NLP:
    
    def __init__(self) -> None:
        self.model = "gpt-4o-mini"
        self.client = OpenAI()

    def classifyFishing(self, question) -> None:
        if question != None:
            thread = self.client.beta.threads.create()
            message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
            )

            run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id = 'asst_VlzcLJVSi1Lw4WWxTFcCRDJK',
            )

            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                result = messages.data
            else:
                result = run.status

        return result