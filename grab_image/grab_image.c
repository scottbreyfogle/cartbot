#include <stdio.h>
#include <X11/Xlib.h>
#include <giblib/giblib.h>

Display *disp;
Screen *scr;
Window root;

/*
Window get_window_contents(Window target) {
    Atom state = XInternAtom(display, "WM_STATE", True);
    if (state == None) # No border / wm
        return target;

    int format;
    unsigned char *data;
    unsigned long after, items;
    int status = XGetWindowProperty(display, target, state, 0l, 0l, False,
            (Atom) AnyPropertyType, &type, &forma, &items, &after, &data);
    if (status == Success && type != None) {
        return target;
    }
}
*/

int get_geometry(Window target, int *rx, int *ry, int *rw, int *rh)
{
    Window child;
    XWindowAttributes attr;
    int stat;

    /* get windowmanager frame of window */
    if (target != root) {
      unsigned int d, x;
      int status;

      status = XGetGeometry(disp, target, &root, &x, &x, &d, &d, &d, &d);
      if (status != 0) {
        Window rt, *children, parent;

        for (;;) {
          /* Find window manager frame. */
          status = XQueryTree(disp, target, &rt, &parent, &children, &d);
          if (status && (children != None))
            XFree((char *) children);
          if (!status || (parent == None) || (parent == rt))
            break;
          target = parent;
        }
        /* Get client window. */
        // target = scrot_get_client_window(disp, target);
        XRaiseWindow(disp, target);
      }
    }
    stat = XGetWindowAttributes(disp, target, &attr);
    if ((stat == False) || (attr.map_state != IsViewable))
      return 0;
    *rw = attr.width;
    *rh = attr.height;
    XTranslateCoordinates(disp, target, root, 0, 0, rx, ry, &child);
    return 1;
}

void crop_image(Screen *scr, int *rx, int *ry, int *rw, int *rh) {
    if (*rx < 0) {
      *rw += *rx;
      *rx = 0;
    }
    if (*ry < 0) {
      *rh += *ry;
      *ry = 0;
    }
    if ((*rx + *rw) > scr->width)
      *rw = scr->width - *rx;
    if ((*ry + *rh) > scr->height)
      *rh = scr->height - *ry;
}

Imlib_Image grab_focused(void)
{
    // Setup x stuff
    disp = XOpenDisplay(NULL);
    if(!disp)
        printf("Can't open X display. Have fun with that.");
    scr = ScreenOfDisplay(disp, DefaultScreen(disp));
    root = RootWindow(disp, XScreenNumberOfScreen(scr));

    // Info about current window
    int rx = 0, ry = 0, rw = 0, rh = 0;
    Window target = None;
    int ignored;

    XGetInputFocus(disp, &target, &ignored); // Get current window
    if (!get_geometry(target, &rx, &ry, &rw, &rh)) { // Load window's boundaries
        return NULL;
    }
    crop_image(scr, &rx, &ry, &rw, &rh); // truncate boundaries to viewable area

    return gib_imlib_create_image_from_drawable(root, 0, rx, ry, rw, rh, 1);
}

int main(int argc, char **argv) {
    char *filename = argv[1];
    Imlib_Image image = grab_focused();
    Imlib_Load_Error err;
    printf("Saving to %s.\n", filename);
    //gib_imlib_save_image_with_error_return(image, filename, &err);
    if (err) {
        printf("Saving to %s failed\n", filename);
        return 1;
    }
    return 0;
}
