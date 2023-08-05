microquest - gamify anything

[![asciicast](https://asciinema.org/a/7yar4jllfpm9hsgn5yom6kr16.png)](https://asciinema.org/a/7yar4jllfpm9hsgn5yom6kr16)

# installation

	pip install microquest

# usage

	Usage: mq [OPTIONS] COMMAND [ARGS]...

	Options:
	  --help  Show this message and exit.

	Commands:
	  init      init the game
	  importq   import a quest file

	  quests    print quests
	  add       add a quest
	  rm        remove a quest

	  do        do a quest
	  skip      skip a quest
	  buy       buy something (negative value quest)

	  complete  complete a quest, remove it
	  fail      fail a quest, remove it

	  log       print log
	  status    get player status

	  table     print xp table

# halp

first init the game with `mq init`

add some sample quests with mq import `quest-samples.ini`

add bash completions with `source completion.sh`

shop items are represented as negative value quests, use buy action.

# ideas

* whan to use microquest for coding? You can for add a post-commit containing `mq do commit`  hook to your global git configuration, do the same for pre-push and post-rewrite then set your class to `coder` then add `commit`, `push` and `rewrite` quests
* you have too much privacy? microblog your progress! the logfile in `~/.config/microquest/log` is compatible with [twtxt](https://github.com/buckket/twtxt)
* share you quests files among a team

# todo

* --charfile option
* 1 log per char
* publish to pip
* do multiple actions in one command?
