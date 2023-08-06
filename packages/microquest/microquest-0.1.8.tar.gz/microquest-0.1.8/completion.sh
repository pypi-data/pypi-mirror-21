_mq_completion() {
    COMPREPLY=( $( env COMP_WORDS="${COMP_WORDS[*]}" \
                   COMP_CWORD=$COMP_CWORD \
                   _MQ_COMPLETE=complete $1 ) )
    return 0
}

complete -F _mq_completion -o default mq;
