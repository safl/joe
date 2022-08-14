from pathlib import Path

GUEST_NAME_DEFAULT="emujoe"

def qemu_img(cijoe, args=[]):
    """Helper function wrapping around 'qemu_img'"""

    return cijoe.run_local(f"{cijoe.config['qemu']['img_bin']} " + " ".join(args))


def qemu_system(cijoe, args=[]):
    """Wrapping the qemu system binary"""

    return cijoe.run_local(f"{cijoe.config['qemu']['system_bin']}" + " ".join(args))


def guest_init(cijoe, guest_name=None):
    """Create guest file layout"""

    if guest_name is None:
        guest_name = GUEST_NAME_DEFAULT

    guest = cijoe.config["qemu"].get(guest_name)
    guest["path"] = Path(guest["path"])

    rcode, _ = cijoe.run_local(f"mkdir -p {guest['path']}")

    return rcode

def guest_start(cijoe, guest_name=None):
    """Start a guest"""

    if guest_name is None:
        guest_name = GUEST_NAME_DEFAULT

    args = []
    args.append("-machine ")


  if [[ -v QEMU_GUEST_SMP ]]; then
    _args="$_args -smp ${QEMU_GUEST_SMP}"
  fi

  # NOTE: how does this behave when cpu=host and the host is e.g. a Ryzen?
  if [[ -v QEMU_GUEST_IOMMU && "$QEMU_GUEST_IOMMU" != "0" ]]; then
    _args="$_args -device intel-iommu,pt=on,intremap=on"
  fi

  _args="$_args -m ${QEMU_GUEST_MEM}"

  # optionally boot from iso
  if [[ -n "${QEMU_GUEST_BOOT_ISO}" ]]; then
    _args="$_args -boot d -cdrom ${QEMU_GUEST_BOOT_ISO}"
  fi

  # boot drive
  _args="$_args -blockdev ${QEMU_GUEST_BOOT_IMG_FMT},node-name=boot,file.driver=file,file.filename=${QEMU_GUEST_BOOT_IMG}"
  _args="$_args -device virtio-blk-pci,drive=boot"

  # network interface with a single port-forward
  _args="$_args -netdev user,id=n1,ipv6=off,hostfwd=tcp::${QEMU_GUEST_SSH_FWD_PORT}-:22"
  _args="$_args -device virtio-net-pci,netdev=n1"

  # pidfile
  _args="$_args -pidfile ${QEMU_GUEST_PIDFILE}"

  # optionally boot specific kernel
  if [[ -v QEMU_GUEST_KERNEL && "${QEMU_GUEST_KERNEL}" == "1" ]]; then
    _args="$_args -kernel \"${QEMU_GUEST_PATH}/bzImage\""
    _args="$_args -append \"root=/dev/vda1 vga=0 console=ttyS0,kgdboc=ttyS1,115200 ${QEMU_GUEST_APPEND}\""
  fi

  # qemu monitor
  _args="$_args -monitor unix:${QEMU_GUEST_PATH}/monitor.sock,server,nowait"

  case ${QEMU_GUEST_CONSOLE} in
  sock)
    _args="$_args -display none"
    _args="$_args -serial unix:${QEMU_GUEST_PATH}/serial.sock,server,nowait"
    _args="$_args -daemonize"
    ;;

  file)
    _args="$_args -display none"
    _args="$_args -serial file:${QEMU_GUEST_PATH}/serial.txt"
    _args="$_args -daemonize"
    ;;

  stdio)
    _args="$_args -nographic"
    _args="$_args -serial mon:stdio"
    ;;
  esac

  if [[ -v QEMU_GUEST_HOST_SHARE ]]; then
    _args="$_args -virtfs fsdriver=local,id=fsdev0,security_model=mapped,mount_tag=hostshare,path=${QEMU_GUEST_HOST_SHARE}"
  fi



    pass
