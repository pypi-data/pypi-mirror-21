microquest - CLI to gamify anything

# installation

microquest requires python >= 3.6

	pip3 install microquest

# usage

the following asciicast does not reflect the current state of the game but will give you a hint of how it could be used:

[![asciicast](https://asciinema.org/a/7yar4jllfpm9hsgn5yom6kr16.png)](https://asciinema.org/a/7yar4jllfpm9hsgn5yom6kr16)

	usage: mq [-h]
		  {init,i,importq,I,status,S,log,l,table,t,add,a,quests,q,rm,r,do,d,buy,b,complete,c,skip,s,fail,f}
		  ...

	optional arguments:
	  -h, --help            show this help message and exit

	subcommands:
	  {init,i,importq,I,status,S,log,l,table,t,add,a,quests,q,rm,r,do,d,buy,b,complete,c,skip,s,fail,f}
				additional help
	    init (i)            init game
	    importq (I)         import a quest file
	    status (S)          get player status
	    log (l)             print log
	    table (t)           print xp table
	    add (a)             add a quest
	    quests (q)          list quests
	    rm (r)              remove a quest
	    do (d)              do/buy a quest
	    buy (b)             buy something
	    complete (c)        complete a quest
	    skip (s)            skip a quest
	    fail (f)            fail a quest
	use -h for help


# halp

add some sample quests with `mq importq contrib/sample-quests/quest-samples.ini`

add bash completions with eval "$(register-python-argcomplete mq)"

shop items are represented as negative value quests, use buy action.

# how to integrate with git

do not run those commands blindly:

	mkdir -p ~/.git_templates/hooks
	echo "mq do commit" > ~/.git_templates/hooks/post-commit
	echo "mq do push" > ~/.git_templates/hooks/pre-push
	chmod +x ~/.git_templates/hooks/*
	git config --global init.templatedir '~/.git_templates'
	mq add commit "git commit"
	mq add push "git push" 80

then do git init in every of your repository to add the local hooks

# ideas

* you have too much privacy? microblog your progress! the logfile in `~/.config/microquest/log` is compatible with [twtxt](https://github.com/buckket/twtxt)
* share you quests files among a team
* contribute quests/scripts/wrappers in `contrib/` with a pull request

# changelog

## 0.1.9

* fix import error

## 0.1.8

* start rewrite for future implementation of http/web API
* add --pager flag
* add aliases

## 0.1.7

* add --multiplier option (usefull for batch update or combos)

## 0.1.6

* add --silent flag
* update contrib/

	
# todo

* --charfile option
* 1 log per char
