/* hybrid-detect:
 *
 * Detect which GPU in a hybrid graphics configuration should be
 * used
 *
 * Authored by:
 *   Alberto Milone
 *   Evan Broder
 *
 * Modified for Fedora by:
 *   Xiao-Long Chen
 * 
 * Copyright (C) 2011 Canonical Ltd
 * 
 * Based on code from ./hw/xfree86/common/xf86pciBus.c in xorg-server
 *
 * Copyright (c) 1997-2003 by The XFree86 Project, Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE COPYRIGHT HOLDER(S) OR AUTHOR(S) BE LIABLE FOR ANY CLAIM, DAMAGES OR
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 *
 * Except as contained in this notice, the name of the copyright holder(s)
 * and author(s) shall not be used in advertising or otherwise to promote
 * the sale, use or other dealings in this Software without prior written
 * authorization from the copyright holder(s) and author(s).
 *
 *
 * Build with `gcc -o hybrid-detect hybrid-detect.c $(pkg-config --cflags --libs pciaccess)`
 */

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pciaccess.h>
#include <sys/utsname.h>

#define PCI_CLASS_PREHISTORIC           0x00

#define PCI_CLASS_DISPLAY               0x03

#define PCI_CLASS_MULTIMEDIA            0x04
#define PCI_SUBCLASS_MULTIMEDIA_VIDEO   0x00

#define PCI_CLASS_PROCESSOR             0x0b
#define PCI_SUBCLASS_PROCESSOR_COPROC   0x40

#define PCIINFOCLASSES(c)                                               \
    ( (((c) & 0x00ff0000) == (PCI_CLASS_PREHISTORIC << 16))             \
      || (((c) & 0x00ff0000) == (PCI_CLASS_DISPLAY << 16))              \
      || ((((c) & 0x00ffff00)                                           \
           == ((PCI_CLASS_MULTIMEDIA << 16) | (PCI_SUBCLASS_MULTIMEDIA_VIDEO << 8)))) \
      || ((((c) & 0x00ffff00)                                           \
           == ((PCI_CLASS_PROCESSOR << 16) | (PCI_SUBCLASS_PROCESSOR_COPROC << 8)))) )

#define FILENAME "/var/lib/hybrid-detect/last_gfx_boot"

static struct pci_slot_match match = {
    PCI_MATCH_ANY, PCI_MATCH_ANY, PCI_MATCH_ANY, PCI_MATCH_ANY, 0
};

/* Get the master link of an alternative */
char* get_alternative_link(char *arch_path, char *pattern) {
    char *temp;

    /* Check if we're dealing with the Xorg configuration file for setting
     * the ModulePath */
    if (strcmp(arch_path, "00-gfx") == 0) {
        /* Intel graphics card */
        if (strcmp(pattern, "mesa") == 0) {
            asprintf(&temp, "/etc/X11/modulepath.intel.conf");
            return temp;
        }
        else if (strcmp(pattern, "nvidia") == 0) {
            asprintf(&temp, "/etc/X11/modulepath.nvidia.conf");
            return temp;
        }
    }
    else if (strcmp(arch_path, "nvidia-lib") == 0 || 
             strcmp(arch_path, "nvidia-lib64") == 0) {
        /* Disable nVidia libraries by setting alternative to /dev/null
         * mesa libraries are stored in /usr/lib{,64}, so the ld.so.conf.d
         * files can just be disabled. */
        if (strcmp(pattern, "nvidia") == 0) {
            asprintf(&temp, "/usr/share/nvidia/%s.conf", arch_path);
            return temp;
        }
        else if (strcmp(pattern, "mesa") == 0) {
            asprintf(&temp, "/dev/null");
            return temp;
        }
    }
    else {
        return NULL;
    }
}

int main(int argc, char *argv[]) {

    /* Check root privileges */
    uid_t uid=getuid();
    if (uid != 0) {
        fprintf(stderr, "Error: please run this program as root\n");
        exit(1);
    }
    
    pci_system_init();

    struct pci_device_iterator *iter = pci_slot_match_iterator_create(&match);
    if (!iter)
        return 1;

    FILE *pfile = NULL;
    int last_vendor = 0;
    int last_device = 0;
    char *arch_path = NULL;

    /* Read from last boot gfx */
    pfile = fopen(FILENAME, "r");
    if (pfile == NULL) {
        fprintf(stderr, "I couldn't open %s for reading.\n", FILENAME);
        /* Create the file for the 1st time */
        pfile = fopen(FILENAME, "w");
        printf("Create %s for the 1st time\n", FILENAME);
        if (pfile == NULL) {
            fprintf(stderr, "I couldn't open %s for writing.\n",
                    FILENAME);
            exit(1);
        }
        fprintf(pfile, "%x:%x\n", 0x0, 0x0);
        fflush(pfile);
        fclose(pfile);
        /* Try again */
        pfile = fopen(FILENAME, "r");
    }
    fscanf(pfile, "%x:%x\n", &last_vendor, &last_device);
    fclose(pfile);

    struct pci_device *info;
    while ((info = pci_device_next(iter)) != NULL) {
        if (PCIINFOCLASSES(info->device_class) &&
            pci_device_is_boot_vga(info)) {
            //printf("%x:%x\n", info->vendor_id, info->device_id);
            char *driver = NULL;
            if (info->vendor_id == 0x10de) {
                driver = "nvidia";
            }
            else if (info->vendor_id == 0x8086) {
                driver = "mesa";
            }
            else {
                fprintf(stderr, "No hybrid graphics cards detected\n");
                break;
            }

            pfile = fopen(FILENAME, "w");
            if (pfile == NULL) {
                fprintf(stderr, "I couldn't open %s for writing.\n",
                        FILENAME);
                exit(1);
            }
            fprintf(pfile, "%x:%x\n", info->vendor_id, info->device_id);
            fflush(pfile);
            fclose(pfile);

            /* Change the login a little bit:
             * In Ubuntu's version, last_vendor is checked to see if it's
             * NOT 0, then checked to see if it matches the current vendor
             * ID. The problem is that last_vendor defaults to 0, which
             * means that update-alternatives won't be run if last_gfx_boot
             * is missing or empty (initial installation). However,
             * update-alternatives needs to run because the graphics card
             * used during the installation could be either the Intel
             * graphics card or the nVidia graphics card.
             *
             * This can altered to run update-alternatives if last_vendor
             * equals 0 (last_gfx_boot is missing or empty) OR if
             * last_vendor does not match the current vendor ID. */
            if (last_vendor == 0 || last_vendor != info->vendor_id) {
                printf("Gfx was changed in the BIOS\n");

                struct utsname uts;
                if (uname(&uts) < 0) {
                    fprintf(stderr, "Failed to detect CPU architecture\n");
                    break;
                }
                if (strcmp(uts.machine, "x86_64") == 0) {
                    arch_path = "nvidia-lib64";
                }
                else if (strcmp(uts.machine, "i686") == 0) {
                    arch_path = "nvidia-lib";
                }
                else {
                    fprintf(stderr,
                            "%s is not supported for hybrid graphics\n",
                            uts.machine);
                    break;
                }

                char *alternative = NULL;
                alternative = get_alternative_link(arch_path, driver);

                if (alternative == NULL) {
                    fprintf(stderr, "Error: no alternative found\n");
                    break;
                }
                else {
                    /* Set the alternative */
                    printf("Select %s for %s.conf\n", alternative, arch_path);
                    char command[200];

                    /* Set alternative for nVidia libraries */
                    sprintf(command, "update-alternatives --set %s.conf %s",
                            arch_path, alternative);
                    system(command);
                    free(alternative);

                    /* Set alternative for nvidia libraries (xorg-x11-drv-nvidia-libs) */
                    if (strcmp(arch_path, "nvidia-lib64") == 0 &&
                        access("/usr/share/nvidia/nvidia-lib.conf", F_OK) == 0) {
                        /* If on 64 bit system and 32 bit libraries are installed,
                         * then also update the alternatives for the 32 bit
                         * libraries. */
                        alternative = get_alternative_link("nvidia-lib", driver);
                        printf("Select %s for nvidia-lib.conf\n", alternative);

                        sprintf(command, "update-alternatives --set nvidia-lib.conf %s",
                                alternative);
                        system(command);
                        free(alternative);
                    }

                    /* Set alternative for Xorg configuration file */
                    alternative = NULL;
                    alternative = get_alternative_link("00-gfx", driver);
                    printf("Select %s for 00-gfx.conf\n", alternative);

                    sprintf(command, "update-alternatives --set 00-gfx.conf %s",
                            alternative);
                    system(command);
                    free(alternative);

                    /* call ldconfig */
                    system("LDCONFIG_NOTRIGGER=y ldconfig");

                }
            }
            else {
                printf("No gfx change\n");
                break;
            }
            break;
        }
    }
    pci_iterator_destroy(iter);
    return 0;
}
