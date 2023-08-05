# bash quest

in my experience this works but slows down bash prompt a bit

use at your own risks

add this at the end of your ~/.bashrc:

	declare -r PROMPT_COMMAND='if [ $? -ne 0 ]; then mq buy bashnok --silent; else mq do bashok --silent;fi'

then `mq importq bash-quest.ini`

* You'll gain 1 xp after each correct bash command
* You'll lose 5 coin after each incorrect bash command
* Running a bash script only runs mq once.
