#include <Python.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/features2d/features2d.hpp>

extern "C" {

static PyObject *
create(PyObject *self, PyObject *args)
{
    const char *filename = NULL;
    const char *type = NULL;
	float initFeatureScale = 0.0f;
	int featureScaleLevels = 0;
	float featureScaleMul = 0.0f;
	int initXyStep = 0;
	int initImgBound = 0;
	
    if (!PyArg_ParseTuple(args, "ssfifii", &filename, &type,
							&initFeatureScale,
							&featureScaleLevels,
							&featureScaleMul,
							&initXyStep,
							&initImgBound)) {
		return Py_BuildValue("s", "");
	}

	// 画像ファイルを読み込む．
	cv::Mat img = cv::imread(filename);
	if (img.empty()) {
    	return Py_BuildValue("s", "");
	}

	cv::DenseFeatureDetector detector(
		initFeatureScale,
		featureScaleLevels,
		featureScaleMul,
		initXyStep,
		initImgBound,
		false,
		false
	);
	std::vector<cv::KeyPoint> keypoints;
	detector.detect(img, keypoints);

	// 記述子として次のいずれかを指定する
	// FAST, GFTT, SIFT (nonfree), SURF (nonfree),
	// MSER, STAR, ORB, BRISK, FREAK, BRIEF
	cv::Ptr<cv::DescriptorExtractor> extractor = cv::DescriptorExtractor::create(type);
	cv::Mat descriptors;
	extractor->compute(img, keypoints, descriptors);
	std::ostringstream stream;
	stream << cv::format(descriptors, "csv");
	return Py_BuildValue("s", stream.str().c_str());
}

static char feature_doc[] = "C extention module example\n";

static PyMethodDef methods[] = {
    {"create", create, METH_VARARGS, "return create.\n"},
    {NULL, NULL, 0, NULL}
};

void initfeature(void)
{
    Py_InitModule3("feature", methods, feature_doc);
}
}
