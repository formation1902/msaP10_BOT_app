from botbuilder.dialogs.prompts import Prompt, PromptOptions,PromptRecognizerResult
from botbuilder.core.turn_context import TurnContext
from botbuilder.schema import ActivityTypes
from recognizers_text import Culture, ModelResult,StringUtility



from typing import Callable, Dict
import enum

class EmailPrompt (Prompt):
    def __init__(self,         dialog_id,        validator : object = None,        defaultLocale = None):
     super().__init__(dialog_id, validator=validator)
     
     if defaultLocale is None:
        defaultLocale = Culture.English

     self._defaultLocale = defaultLocale

    async def on_prompt(        self,         turn_context: TurnContext,         state: Dict[str, object],         options: PromptOptions,         is_retry: bool,     ):
        if not turn_context:
            raise TypeError("turn_context Can’t  be none")
        if not options:
            raise TypeError("options Can’t  be none")

        if is_retry and options.retry_prompt is not None:
            await turn_context.send_activity(options.retry_prompt)
        else:
            if options.prompt is not None:
                await turn_context.send_activity(options.prompt)    

    async def on_recognize(self,        turn_context: TurnContext,         state: Dict[str, object],         options: PromptOptions,     ) -> PromptRecognizerResult:  
        if not turn_context:
            raise TypeError("turn_context cannt be none")

        if turn_context.activity.type == ActivityTypes.message:
            usertext = turn_context.activity.text
        
        turn_context.activity.locale = self._defaultLocale

        recong = SequenceRecognizer(turn_context.activity.locale)
        mode = recong.get_email_model()
        mode_result = mode.parse(usertext)

        prompt_result = PromptRecognizerResult()

        if len(mode_result) > 0 and len(mode_result[0].resolution) > 0:
            prompt_result.value = mode_result[0].resolution["value"]
            prompt_result.succeeded = True

        return prompt_result
    
    

