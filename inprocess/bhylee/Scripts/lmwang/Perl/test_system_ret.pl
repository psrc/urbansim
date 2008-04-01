$status = system("non_exist.bat");
die "$program exited funny: $?"; #if $status != 0;
