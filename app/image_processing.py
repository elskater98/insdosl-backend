import os
import matplotlib.pyplot as plt
from deepface import DeepFace
from retinaface import RetinaFace


class Recognition():

    def do_recognition(self, image=None, actions=None):
        if not image:
            return False
        tmp_file = '/tmp/tmp_file.jpg'
        if len(self.check_faces(image)) == 1:
            moods = [self.analyze(tmp_file, actions)]
        elif len(self.check_faces(image)) > 1:
            faces = RetinaFace.extract_faces(
                img_path=image,
                align=True)
            moods = []
            for face in faces:
                plt.imshow(face)
                plt.savefig(tmp_file)
                try:
                    moods.append(self.analyze(tmp_file, actions))
                except ValueError:
                    continue
            os.remove(tmp_file)

        return {
            'dominant_emotion': max([m['dominant_emotion'] for m in moods]),
            }

    def analyze(self, image=None, actions=None):
        if not image:
            return {}
        if not actions:
            actions = ['emotion']
        obj = DeepFace.analyze(
            img_path=image,
            actions=actions,
            )
        return obj

    def check_faces(self, image=None):
        if not image:
            return {}
        faces = RetinaFace.detect_faces(image)
        return faces
