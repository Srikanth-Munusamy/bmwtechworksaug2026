import IconButton from '../../atoms/IconButton/IconButton';
import ClientSelect from '../../atoms/Select/Select';
import ModelSelect from '../../atoms/Select/Select';
import {plus,mic} from 'lucide-react';
import SendButton from '../../atoms/Button/Button';
export default function ToolComposer({ 
    message,clients,models,onClientChange,onModelChange,onSend}) {

     return(
        <div className="flex items-center gap-4">
          <IconButton icon={plus} label="Add attachment"
            className="grid h-11 w-11 rounded-full 
            place-items-center text-neutral-900 transition hover:bg-neutral-200"
            onClick={() => {console.log('Add attachment clicked')}} />

          <div className="flex items-center gap-4">
          <ClientSelect options={clients} onChange={onClientChange}/>
          <ModelSelect options={models} onChange={onModelChange}/>
      
          <IconButton icon={mic} label="Record audio" 
            className="grid h-11 w-11 rounded-full 
            place-items-center text-neutral-900 transition hover:bg-neutral-200"
            onClick={() => {console.log('Record audio clicked')}} />

          <SendButton onClick={onSend} disabled={!message} />
        </div>
        </div>
     )


    }