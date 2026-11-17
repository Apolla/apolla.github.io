读取视频包 ------> 解码  ------> 显示


视频流程：
 
1)读取线程：读取视频包，推入videoq队列中
```objectivec
read_thread{
    ret = stream_component_open(ffp, st_index[AVMEDIA_TYPE_VIDEO]);{
        is->video_tid = SDL_CreateThreadEx(&is->_video_tid, video_thread, ffp, "ff_video_dec");
    }
 
    for (;;) {
        if (is->abort_request)
            break;
 
        ret = av_read_frame(ic, pkt);
        packet_queue_put(&is->videoq, pkt);   //将获取到的视频包推入videoq队列中
    }
}
```

 
 
2）解码线程
软解：从videoq队列中获取视频包，解码视频帧放入pictq列表中
硬解：从videoq队列中获取视频包，推送MediaCodec解码，获取解码outputbuffer index并存储在pictq列表中
```objectivec
video_thread{
    ffpipenode_run_sync(ffp->node_vdec);{
        node->func_run_sync(node);{ // decoder_from_android_mediacodec 硬解流程
            SDL_CreateThreadEx(enqueue_thread_func){
                while (!q->abort_request) {
                    feed_input_buffer{ 
                        ffp_packet_queue_get_or_buffering
                        SDL_AMediaCodec_dequeueInputBuffer
                        input_buffer_ptr = SDL_AMediaCodec_getInputBuffer
                        memcpy(input_buffer_ptr, d->pkt_temp.data, copy_size);
                        SDL_AMediaCodec_queueInputBuffer
                    }
                }
            }
            while{
                drain_output_buffer{
                     output_buffer_index = SDL_AMediaCodec_dequeueOutputBuffer   
                }
            }
        }
    }
 
 
 
    node->func_run_sync(node);{ // decoder_from_ffplay 软解流程
        func_run_sync{
            ffp_video_thread{
                ffplay_video_thread{
                     for (;;) {
                         get_video_frame(ffp, frame);{
                             decoder_decode_frame(ffp, &is->viddec, frame){
                                  avcodec_decode_video2(d->avctx, frame, &got_frame);
                                  || avcodec_decode_audio4(d->avctx, frame, &got_frame);
                             }
                         }
                         queue_picture(ffp, frame, pts, duration){
                             vp = frame_queue_peek_writable(&is->pictq);
                             SDL_VoutFFmpeg_ConvertFrame(vp->bmp, src_frame){
                      
                             }
                         }
                         frame_queue_push(&is->pictq);
                     }
                }
            }
        }
    }
}
```

 
 
3）显示线程
硬解：由MediaCodec configure Surface，自动完成视频帧的渲染
软解：从pictq列表中获取视频帧，写入nativewindows视频缓冲中渲染
```objectivec
video_refresh_thread {
   IJKFF_Pipenode *node = ffpipeline_open_video_output(ffp->pipeline, ffp);
      ffpipenode_run_sync(node);{
          ffp_video_refresh_thread(opaque->ffp);{
              ffplay_video_refresh_thread{
                  while(!is->abort_request) {
                      video_refresh(ffp, &remaining_time);{
                          video_image_display2{
                             vp = frame_queue_peek(&is->pictq);
                             SDL_VoutDisplayYUVOverlay(ffp->vout, vp->bmp);{
                                 SDL_VoutOverlayAMediaCodec_releaseFrame  or
                                 SDL_Android_NativeWindow_display_l
                             }
                          }
                      }
                  }
              }
          }
      }    
   }
}
```



