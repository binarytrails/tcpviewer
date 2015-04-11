kill -9 `ps ax | grep node | grep meteor | awk '{print $1}'`

