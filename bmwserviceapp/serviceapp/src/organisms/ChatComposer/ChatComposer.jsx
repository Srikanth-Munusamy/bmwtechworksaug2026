import PromptInput from '../../molecules/PromptInput/PromptInput';
import { useState } from 'react';
export default function ChatComposer() {
     //create state hook
     const [message, setMessage] = useState('');
     
     const changeMessage = (e) => setMessage(e.target.value);
     const handleKeyDown = (e) => {
         if (e.key === 'Enter') {
             e.preventDefault();
             // handle sending the message here
         }
     };

    return (
        <section>
            <PromptInput value={message} onChange={changeMessage} 
            placeholder="Type your query..." 
            onKeyDown={handleKeyDown} className="h-33 w-full 
            resize-none border-0 transparent px-7 py-7 text-xl leading-relaxed
            text-neutral-900 outline-none placeholder:text-neutral-400
            sm:text-2xl
            "
            
            />
        </section>
    );
}