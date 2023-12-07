#include <gst/gst.h>
#include <gst/rtsp-server/rtsp-server.h>

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char launch_cmd[256];

const char *getVideoSourceType(const char *video_src)
{
    if (strncmp(video_src, "/dev/video", 10) == 0)
    {
        return "v4l2src";
    }
    else if (video_src, "rtsp://", 7 == 0)
    {
        return "rtsp";
    }
    else
    {
        return NULL;
    }
}

void getLauchCommand(const char *video_src)
{
    const char *video_type = getVideoSourceType(video_src);
    if (strcmp(video_type, "v4l2src") == 0)
    {
        launch_cmd[0] = '(';
        strcat(launch_cmd, video_type);
        strcat(launch_cmd, " device=");
        strcat(launch_cmd, video_src);
        strcat(launch_cmd,
               " ! videoconvert ! video/x-raw,width=640,height=480 ! x264enc ! rtph264pay name=pay0 pt=96 )");
    }
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage: %s path-to-video-source rtsp-server-port", argv[0]);
        return EXIT_FAILURE;
    }
    char *video_src = argv[1];
    char *rtsp_server_port = argv[2];

    //////////////////////////////////

    getLauchCommand(video_src);
    printf("%s\n", launch_cmd);

    //////////////////////////////////

    GMainLoop *loop;
    GstRTSPServer *server;
    GstRTSPMountPoints *mounts;
    GstRTSPMediaFactory *factory;

    gst_init(NULL, NULL);
    loop = g_main_loop_new(NULL, FALSE);
    server = gst_rtsp_server_new();
    printf("CHECKPOINT.\n");

    //////////////////////////////////

    gst_rtsp_server_set_service(server, rtsp_server_port);
    printf("CHECKPOINT.\n");
    
    //////////////////////////////////

    mounts = gst_rtsp_server_get_mount_points(server);
    factory = gst_rtsp_media_factory_new();
    gst_rtsp_media_factory_set_launch(factory, launch_cmd);
    printf("CHECKPOINT.\n");
    gst_rtsp_media_factory_set_shared(factory, TRUE);
    gst_rtsp_mount_points_add_factory(mounts, "/stream", factory);
    printf("CHECKPOINT.\n");
    g_object_unref(mounts);
    gst_rtsp_server_attach(server, NULL);
    printf("CHECKPOINT.\n");

    printf("Stream ready at: rtsp://127.0.0.1:%s/stream", rtsp_server_port);
    g_main_loop_run(loop);

    return EXIT_SUCCESS;
}

/*
gcc rtsp.c -o rtsp `pkg-config --cflags --libs gstreamer-1.0 gstreamer-rtsp-server-1.0`
*/
