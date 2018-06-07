function doSomething()
{
        local retTmp=$(mktemp)
        local lock="/tmp/do.lock"
        touch $lock
        (
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_set_runnable"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_switch_proc"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_kill"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_reap"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_reparent"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_send_proc"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_recv_proc"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_reply_wait_proc"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_call_proc"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_create"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_close"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_dup"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_dup2"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_lseek"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_map_pcipage"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_iommu_root"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_iommu_pdpt"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_iommu_pd"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_iommu_pt"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_iommu_frame"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_map_iommu_frame"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_reclaim_iommu_frame"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_reclaim_iommu_root"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_vector"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_reclaim_vector"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_intremap"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_reclaim_intremap"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_ack_intr"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_io_bitmap"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_alloc_port"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_sys_reclaim_port"
		docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c "git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make > /dev/null; make hv6-verify -- -v --failfast HV6.test_extintr"

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
