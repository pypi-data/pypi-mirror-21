安卓自动化测试工具包
集成FPS收集收集器：
device.fps_stats_start()
device.fps_stats_start("SurfaceView")
result=device.fps_stats_stop()
result=device.fps_stats_stop("per_fps")