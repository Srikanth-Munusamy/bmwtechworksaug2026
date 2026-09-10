import NavigationButton from '../../atoms/NavigationButton/NavigationButton';
import {Folder, Files, Monitor, GitBranchPlus} from 'lucide-react';
export default function QuickLinks() {
  return (
   <nav className="mx-auto flex min-h-16 w-[calc(100%-24px)] max-w-266.25 items-center gap-6 overflow-x-auto rounded-b-2xl bg-neutral-50 px-5 py-3 sm:gap-8">
  <NavigationButton icon={Folder}>Folder</NavigationButton>
  <NavigationButton icon={Files}>Files</NavigationButton>
  <NavigationButton>
    <span className="grid h-7 w-7 place-items-center rounded-lg bg-linear-to-br from-amber-300 via-rose-500 to-indigo-400 text-sm font-bold text-white">
        <GitBranchPlus/>
    </span>
    Plugins
  </NavigationButton>
  <NavigationButton icon={Monitor}>Get desktop app</NavigationButton>


   

   </nav>
  );
}