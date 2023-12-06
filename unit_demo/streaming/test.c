#include <gst/gst.h>

int main(int argc, char *argv[]) {
    // Initialize GStreamer
    gst_init(&argc, &argv);

    // Create a GStreamer pipeline
    GstElement *pipeline = gst_parse_launch("rtspsrc location=rtsp://192.168.77.119:8554/test latency=0 ! rtph264depay ! h264parse ! rtph264pay name=pay0 pt=96", NULL);

    // Start the pipeline
    gst_element_set_state(pipeline, GST_STATE_PLAYING);

    // Main loop
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(loop);

    // Cleanup
    gst_element_set_state(pipeline, GST_STATE_NULL);
    gst_object_unref(GST_OBJECT(pipeline));

    return 0;
}
