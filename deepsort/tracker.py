# from deep_sort.deep_sort.tracker import Tracker as DeepSortTracker
# from deep_sort.tools import generate_detections as gdet
# from deep_sort.deep_sort import nn_matching
# from deep_sort.deep_sort.detection import Detection
from deep_sort.tracker import Tracker as DeepSortTracker
from deep_sort.track import Track as DeepSortTrack
from deep_sort.track import TrackState
from tools import generate_detections as gdet
from deep_sort import nn_matching
from deep_sort.detection import Detection
import numpy as np

class Tracker_class_id(DeepSortTracker):
    def __init__(self, metric, max_iou_distance=0.7, max_age=30, n_init=3):
        super(Tracker_class_id, self).__init__(metric, max_iou_distance, max_age, n_init)
    def _initiate_track(self, detection):
        mean, covariance = self.kf.initiate(detection.to_xyah())
        self.tracks.append(Track_class_id(
            mean, covariance, self._next_id, self.n_init, self.max_age,
            detection.feature, detection.class_id))
        self._next_id += 1

class Track_class_id(DeepSortTrack):
    def __init__(self, mean, covariance, track_id, n_init, max_age,
                 feature=None, class_id=0):
        super(Track_class_id, self).__init__(mean, covariance, track_id, n_init, max_age,
                 feature)
        self.class_id = class_id
    def update(self, kf, detection):
        self.mean, self.covariance = kf.update(
            self.mean, self.covariance, detection.to_xyah())
        self.features.append(detection.feature)
        self.class_id = detection.class_id
        self.hits += 1
        self.time_since_update = 0
        if self.state == TrackState.Tentative and self.hits >= self._n_init:
            self.state = TrackState.Confirmed
    


class Detection_class_id(Detection):
    """
    This class represents a bounding box detection in a single image, with class_id.

    Parameters
    ----------
    tlwh : array_like
        Bounding box in format `(x, y, w, h)`.
    confidence : float
        Detector confidence score.
    feature : array_like
        A feature vector that describes the object contained in this image.
    
    class_id : int
        A int representing the object class

    Attributes
    ----------
    tlwh : ndarray
        Bounding box in format `(top left x, top left y, width, height)`.
    confidence : ndarray
        Detector confidence score.
    feature : ndarray | NoneType
        A feature vector that describes the object contained in this image.

    """
    # def __init__(self, name):
    #     super(Mix, self).__init__(name)
    def __init__(self, tlwh, confidence, feature, class_id):
        super(Detection_class_id, self).__init__(tlwh, confidence, feature)
        # self.tlwh = np.asarray(tlwh, dtype=np.float)
        # self.confidence = float(confidence)
        # self.feature = np.asarray(feature, dtype=np.float32)
        self.class_id = class_id


class Tracker:
    tracker = None
    encoder = None
    tracks = None
    # class_id_list = []

    def __init__(self):
        max_cosine_distance = 0.4
        nn_budget = None

        encoder_model_filename = '/root/autodl-tmp/deep_sort_cv_engineer/model_data/mars-small128.pb'

        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        # self.tracker = DeepSortTracker(metric)
        self.tracker = Tracker_class_id(metric)
        self.encoder = gdet.create_box_encoder(encoder_model_filename, batch_size=128)
        # self.class_id_list = []
        

    def update(self, frame, detections):

        if len(detections) == 0:
            self.tracker.predict()
            self.tracker.update([])  
            self.update_tracks()
            return
        
        # bboxes = np.asarray([d[:-1] for d in detections])
        # print(len(detections), detections)
        # bboxes[:, 2:] = bboxes[:, 2:] - bboxes[:, 0:2]
        # scores = [d[-1] for d in detections]
        bboxes = np.asarray([d[:-2] for d in detections])
        bboxes[:, 2:] = bboxes[:, 2:] - bboxes[:, 0:2]
        scores = [d[-2] for d in detections]
        class_id_list = [d[-1] for d in detections]

        features = self.encoder(frame, bboxes)

        dets = []
        for bbox_id, bbox in enumerate(bboxes):
            dets.append(Detection_class_id(bbox, scores[bbox_id], features[bbox_id], class_id_list[bbox_id]))

        # self.class_id_list = class_id_list
        self.tracker.predict()
        self.tracker.update(dets)
        self.update_tracks()

    def update_tracks(self):
        tracks = []
        # i=0
        for track in self.tracker.tracks: #
            if (not track.is_confirmed()) or (track.time_since_update > 1):
                # i = i+1
                continue
            bbox = track.to_tlbr()
            # bbox = [0,0,0,0]

            track_id = track.track_id
            
            # class_id = self.class_id_list[i]
            class_id = track.class_id

            tracks.append(Track_result(track_id,bbox, class_id))
            # i = i + 1
        self.tracks = tracks

class Track_result:
    track_id = None
    bbox = None
    class_id = None
    def __init__(self, id, bbox, class_id):
        self.track_id = id
        self.bbox = bbox
        self.class_id = class_id
