#include <gst/gst.h>
#include <gst/rtsp-server/rtsp-server.h>

int main(int argc, char *argv[])
{
    GMainLoop *loop;
    GstRTSPServer *server;
    GstRTSPMountPoints *mounts;
    GstRTSPMediaFactory *factory;

    gst_init(&argc, &argv);
    loop = g_main_loop_new(NULL, FALSE);
    server = gst_rtsp_server_new();

    // gst_rtsp_server_set_address(server, "192.168.77.119");
    gst_rtsp_server_set_service(server, "8554");

    mounts = gst_rtsp_server_get_mount_points(server);
    factory = gst_rtsp_media_factory_new();

    gst_rtsp_media_factory_set_launch(factory,
                                      "(v4l2src devive=/dev/video0 ! videoconvert ! video/x-raw,width=640,height=480 ! x264enc ! rtph264pay name=pay0 pt=96 )");

    gst_rtsp_media_factory_set_shared(factory, TRUE);

    gst_rtsp_mount_points_add_factory(mounts, "/stream", factory);

    g_object_unref(mounts);
    gst_rtsp_server_attach(server, NULL);
    g_print("Stream ready at rtsp://127.0.0.1:8554/stream\n");
    g_main_loop_run(loop);
    return 0;
}

/*

sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio

sudo apt-get install libgstrtspserver-1.0-dev gstreamer1.0-rtsp

compile:
gcc rtsp_server.c -o rtsp_server `pkg-config --cflags --libs gstreamer-1.0 gstreamer-rtsp-server-1.0`
*/