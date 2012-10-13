/* Written by: Xiao-Long Chen <chenxiaolong@cxl.epac.to> */

/* Uses some code written by Canonical (see the hybrid-detect source code
 * in their nvidia-common package */

#include <pciaccess.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/utsname.h>
#include <unistd.h>

#define PCI_CLASS_DISPLAY 0x03

#define FILENAME "/var/lib/hybrid-detect/last_gfx_boot"

static struct pci_slot_match match = {
  PCI_MATCH_ANY, PCI_MATCH_ANY, PCI_MATCH_ANY, PCI_MATCH_ANY, 0
};

enum DRIVERS {
  INTEL,
  NVIDIA,
  OPTIMUS
};

enum DRIVERS hybrid_mode;
static int      optimus_status = 0;
static int last_optimus_status = 0;
static int      main_vendor_id = 0;
static int last_main_vendor_id = 0;
static int      main_device_id = 0;
static int last_main_device_id = 0;

void get_devices() {
  pci_system_init();

  struct pci_device_iterator *iterator = pci_slot_match_iterator_create(&match);

  if (iterator == NULL) {
    exit(1);
  }

  int vga_device_count = 0;
  int found_main_gfx = 0;

  struct pci_device *info;
  while ((info = pci_device_next(iterator)) != NULL) {
    if ((info->device_class & 0x00ff0000) == (PCI_CLASS_DISPLAY << 16)) {
      if (pci_device_is_boot_vga(info) && found_main_gfx == 0) {
        if (info->vendor_id == 0x10de) {
          hybrid_mode = NVIDIA;
        }
        else if (info->vendor_id == 0x8086) {
          hybrid_mode = INTEL;
        }
        else {
          fprintf(stderr, "Unknown graphics card: %x:%x\n",
                  info->vendor_id, info->device_id);
          exit(1);
        }

        found_main_gfx = 1;
        main_vendor_id = info->vendor_id;
        main_device_id = info->device_id;

        /* If the bumblebee systemd daemon is enabled, then the system probably
         * has optimus, and we don't need to scan anymore */
        if (optimus_status == 1) {
          break;
        }
      }

      vga_device_count++;
    }
  }

  /* If there's more than one graphics card, assume that the machine has
   * optimus */
  if (vga_device_count > 1) {
    optimus_status = 1;
  }

  if (optimus_status == 1) {
    hybrid_mode = OPTIMUS;
  }
}

void last_boot_gfx() {
  FILE *fptr = NULL;

  fptr = fopen(FILENAME, "r");

  if (fptr == NULL) {
    fprintf(stderr, "Couldn't read from %s\n", FILENAME);

    /* If file doesn't exist, then create it */
    fprintf(stdout, "Creating %s\n", FILENAME);
    fptr = fopen(FILENAME, "w");

    if (fptr == NULL) {
      fprintf(stderr, "Could not write to %s\n", FILENAME);
      exit(1);
    }

    /* Write zero for the optimus status and vendor and device ID's and then
     * continue */
    fprintf(fptr, "%i:%x:%x\n", 0, 0x00, 0x00);
    fflush(fptr);
    fclose(fptr);
    fptr = fopen(FILENAME, "r");
  }

  fscanf(fptr, "%i:%x:%x\n", &last_optimus_status, &last_main_vendor_id,
                                                   &last_main_device_id);
  fclose(fptr);
}

void write_ids() {
  if (last_main_vendor_id != main_vendor_id ||
      last_optimus_status != optimus_status) {
    FILE *fptr;

    fptr = fopen(FILENAME, "w");

    if (fptr == NULL) {
      fprintf(stderr, "Could not write to %s\n", FILENAME);
      exit(1);
    }

    fprintf(fptr, "%i:%x:%x\n", optimus_status, main_vendor_id,
                                                main_device_id);
    fflush(fptr);
    fclose(fptr);
  }
}

void update_alternatives() {
  if (last_main_vendor_id == 0 ||
      last_main_vendor_id != main_vendor_id ||
      last_optimus_status != optimus_status) {
    fprintf(stdout, "Hybrid graphics mode was changed in the BIOS\n");
  }

  struct utsname uts;
  if (uname(&uts) < 0) {
    fprintf(stderr, "Failed to detect CPU architecture\n");
    exit(1);
  }

  switch (hybrid_mode) {
  case INTEL:
  case OPTIMUS:
    system("update-alternatives --set 00-gfx.conf /etc/X11/modulepath.intel.conf");

    if (strcmp(uts.machine, "x86_64") == 0) {
      system("update-alternatives --set nvidia-lib64.conf /dev/null");
    }
    system("update-alternatives --set nvidia-lib.conf /dev/null");
    break;
  case NVIDIA:
    system("update-alternatives --set 00-gfx.conf /etc/X11/modulepath.nvidia.conf");

    if (strcmp(uts.machine, "x86_64") == 0) {
      if (access("/usr/share/nvidia/nvidia-lib.conf", F_OK) == 0) {
        /* Multilib nVidia libraries are installed */
        system("update-alternatives --set nvidia-lib.conf /usr/share/nvidia/nvidia-lib.conf");
      }
      system("update-alternatives --set nvidia-lib64.conf /usr/share/nvidia/nvidia-lib64.conf");
    }
    else {
      system("update-alternatives --set nvidia-lib.conf /usr/share/nvidia/nvidia-lib.conf");
    }
    break;
  }
}

void check_bumblebee() {
  /* Check if the bumblebee daemon is enabled */
  int exit_status = system("systemctl is-enabled bumblebeed.service >/dev/null");
  if (exit_status == -1) {
    fprintf(stderr, "Failed to execute systemctl\n");
    exit(1);
  }
  else if (exit_status == 0) {
    optimus_status = 1;
  }
}

int main(int argc, char *argv[]) {
  /* Must be run as root */
  if (getuid() != 0) {
    fprintf(stderr, "%s must be run as root\n", argv[0]);
    exit(1);
  }

  last_boot_gfx();
  check_bumblebee();
  get_devices();
  write_ids();
  update_alternatives();

  system("LDCONFIG_NOTRIGGER=y ldconfig");
}
