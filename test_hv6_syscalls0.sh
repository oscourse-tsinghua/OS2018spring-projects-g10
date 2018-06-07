function doSomething()
{
        local retTmp=$(mktemp)
        local lock="/tmp/do.lock"
        touch $lock
        (
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_map_pml4"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_map_page_desc"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_map_proc"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_map_dev"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_map_file"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_pdpt"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_pd"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_pt"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_frame"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_copy_frame"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_protect_frame"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_free_pdpt"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_free_pd"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_free_pt"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_free_frame"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_reclaim_page"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_clone_proc"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_set_proc_name"
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
