# bash quest

in my experience this works but slows down bash prompt a bit

use at your own risks

add this at the end of your ~/.bashrc:

	export PROMPT_COMMAND='if [ $? -ne 0 ]; then export bcombo=0; mq do bashnok --silent; else export bcombo=$(($bcombo+1));fi;if [ $bcombo -eq "20" ]; then mq do bashcombo; export bcombo=0 ;fi'

then `mq importq bash-quest.ini`

* You'll gain 50xp after each 20 combo
* You'll lose 5 coin after each incorrect bash command
