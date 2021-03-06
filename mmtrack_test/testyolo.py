# run mot demo
import mmcv
import tempfile
from mmtrack.apis import inference_mot, init_model
mot_config = '../configs/mot/deepsort/deepsort_faster-rcnn_fpn_4e_mot17-private-half.py'
input_video = '../demo/demo.mp4'
imgs = mmcv.VideoReader(input_video)
# build the model from a config file
mot_model = init_model(mot_config, device='cuda:0')
prog_bar = mmcv.ProgressBar(len(imgs))
out_dir = tempfile.TemporaryDirectory()
out_path = out_dir.name
# test and show/save the images
for i, img in enumerate(imgs):
    result = inference_mot(mot_model, img, frame_id=i)
    mot_model.show_result(
            img,
            result,
            show=False,
            wait_time=int(1000. / imgs.fps),
            out_file=f'{out_path}/{i:06d}.jpg')
    prog_bar.update()

output = './mot.mp4'
print(f'\n making the output video at {output} with a FPS of {imgs.fps}')
mmcv.frames2video(out_path, output, fps=imgs.fps, fourcc='mp4v')
out_dir.cleanup()