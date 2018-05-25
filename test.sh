function doSomething()
{
        local retTmp=$(mktemp)
        local lock="/tmp/do.lock"
        touch $lock
        (
                docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/yggdrasil; make; python test_waldisk.py"
                docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/yggdrasil; make; python test_xv6inode.py"
                docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/yggdrasil; make; python test_dirspec.py"
                docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/yggdrasil; make; python test_bitmap.py"
                docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/yggdrasil; make; python test_partition.py"
                docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make; make verify"

                echo $? > $retTmp
                rm -f $lock;
        )&
        while [ -f $lock ]; do
                sleep 0.1
                printf "Please wait... %s \r" $f
                let "t=10#$(date +%N) / 100000000 % 4"
                case $t in
                      0) f="/";;
                      1) f="-";;
                      2) f="\\";;
                      3) f="|";;
                esac
        done
        echo

        local retcode=$(cat $retTmp)
        rm -f $retTmp
        return $retcode
}

doSomething
