_syscalls = [
    "sys_map_pml4",
    "sys_map_page_desc",
    "sys_map_proc",
    "sys_map_dev",
    "sys_map_file",
    "sys_alloc_pdpt",
    "sys_alloc_pd",
    "sys_alloc_pt",
    "sys_alloc_frame",
    "sys_copy_frame",
    "sys_protect_frame",
    "sys_free_pdpt",
    "sys_free_pd",
    "sys_free_pt",
    "sys_free_frame",
    "sys_reclaim_page",
    "clone_proc", # sys_clone
    "sys_set_proc_name",
    "sys_set_runnable",
    "switch_proc", # sys_switch
    "sys_kill",
    "sys_reap",
    "sys_reparent",
    "send_proc", # sys_send
    "recv_proc", # sys_recv
    "reply_wait_proc", # sys_reply_wait
    "call_proc", # sys_call
    "sys_create",
    "sys_close",
    "sys_dup",
    "sys_dup2",
    "sys_lseek",
    "sys_map_pcipage",
    "sys_alloc_iommu_root",
    "sys_alloc_iommu_pdpt",
    "sys_alloc_iommu_pd",
    "sys_alloc_iommu_pt",
    "sys_alloc_iommu_frame",
    "sys_map_iommu_frame",
    "sys_reclaim_iommu_frame",
    "sys_reclaim_iommu_root",
    "sys_alloc_vector",
    "sys_reclaim_vector",
    "sys_alloc_intremap",
    "sys_reclaim_intremap",
    "sys_ack_intr",
    "sys_alloc_io_bitmap",
    "sys_alloc_port",
    "sys_reclaim_port",
    "extintr",
]

for syscall in _syscalls:
    print 'docker run -t amadeuschan/osproject_with_hv6 /bin/sh -c \"git clone https://github.com/oscourse-tsinghua/OS2018spring-projects-g10.git; cd OS2018spring-projects-g10/hv6; make; make hv6-verify -- -v --failfast HV6.test_%s"' % (syscall)
