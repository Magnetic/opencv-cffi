import re

from cffi import FFI


ffi = FFI()


ffi.set_source(
    "_opencv",
    """
    #include "opencv/cv.h"
    #include "opencv/highgui.h"
    #include "opencv2/core/types_c.h"
    #include "opencv2/videoio/videoio_c.h"
    """,
    libraries=[
        "opencv_highgui",
        "opencv_objdetect",
        "opencv_videoio",
    ],
)


ffi.cdef(
    re.sub(
    r"\bCVAPI\(([^)]+)\)",
    r"\1", re.sub(
        r"\bCV_DEFAULT\([^)]+\)",
        "",
    """
/****************************************************************************************\
*                                   Dynamic Data structures                              *
\****************************************************************************************/

/******************************** Memory storage ****************************************/

typedef struct CvMemBlock { ...; } CvMemBlock;
typedef struct CvMemStorage { ...; } CvMemStorage;
typedef struct CvMemStoragePos { ...; } CvMemStoragePos;

/** @brief This is the "metatype" used *only* as a function parameter.

It denotes that the function accepts arrays of multiple types, such as IplImage*, CvMat* or even
CvSeq* sometimes. The particular array type is determined at runtime by analyzing the first 4
bytes of the header. In C++ interface the role of CvArr is played by InputArray and OutputArray.
 */
typedef void CvArr;

typedef struct CvSeq { ...; } CvSeq;

typedef struct CvSize
{
    int width;
    int height;
} CvSize;

/******************************* CvPoint and variants ***********************************/

typedef struct CvPoint { ...; } CvPoint;

/** constructs CvSize structure. */
CvSize  cvSize( int width, int height );

/* "black box" capture structure */
typedef struct CvCapture CvCapture;

/* start capturing frames from video file */
CvCapture* cvCreateFileCapture( const char* filename );

/* start capturing frames from camera: index = camera_index + domain_offset (CV_CAP_*) */
CvCapture* cvCreateCameraCapture( int index );

/* retrieve or set capture properties */
double cvGetCaptureProperty( CvCapture* capture, int property_id );
int    cvSetCaptureProperty( CvCapture* capture, int property_id, double value );

enum
{
    // modes of the controlling registers (can be: auto, manual, auto single push, absolute Latter allowed with any other mode)
    // every feature can have only one mode turned on at a time
    CV_CAP_PROP_DC1394_OFF         = ...,  //turn the feature off (not controlled manually nor automatically)
    CV_CAP_PROP_DC1394_MODE_MANUAL = ..., //set automatically when a value of the feature is set by the user
    CV_CAP_PROP_DC1394_MODE_AUTO = ...,
    CV_CAP_PROP_DC1394_MODE_ONE_PUSH_AUTO = ...,
    CV_CAP_PROP_POS_MSEC       =...,
    CV_CAP_PROP_POS_FRAMES     =...,
    CV_CAP_PROP_POS_AVI_RATIO  =...,
    CV_CAP_PROP_FRAME_WIDTH    =...,
    CV_CAP_PROP_FRAME_HEIGHT   =...,
    CV_CAP_PROP_FPS            =...,
    CV_CAP_PROP_FOURCC         =...,
    CV_CAP_PROP_FRAME_COUNT    =...,
    CV_CAP_PROP_FORMAT         =...,
    CV_CAP_PROP_MODE           =...,
    CV_CAP_PROP_BRIGHTNESS    =...,
    CV_CAP_PROP_CONTRAST      =...,
    CV_CAP_PROP_SATURATION    =...,
    CV_CAP_PROP_HUE           =...,
    CV_CAP_PROP_GAIN          =...,
    CV_CAP_PROP_EXPOSURE      =...,
    CV_CAP_PROP_CONVERT_RGB   =...,
    CV_CAP_PROP_WHITE_BALANCE_BLUE_U =...,
    CV_CAP_PROP_RECTIFICATION =...,
    CV_CAP_PROP_MONOCHROME    =...,
    CV_CAP_PROP_SHARPNESS     =...,
    CV_CAP_PROP_AUTO_EXPOSURE =...,
                                   // user can adjust refernce level
                                   // using this feature
    CV_CAP_PROP_GAMMA         =...,
    CV_CAP_PROP_TEMPERATURE   =...,
    CV_CAP_PROP_TRIGGER       =...,
    CV_CAP_PROP_TRIGGER_DELAY =...,
    CV_CAP_PROP_WHITE_BALANCE_RED_V =...,
    CV_CAP_PROP_ZOOM          =...,
    CV_CAP_PROP_FOCUS         =...,
    CV_CAP_PROP_GUID          =...,
    CV_CAP_PROP_ISO_SPEED     =...,
    CV_CAP_PROP_MAX_DC1394    =...,
    CV_CAP_PROP_BACKLIGHT     =...,
    CV_CAP_PROP_PAN           =...,
    CV_CAP_PROP_TILT          =...,
    CV_CAP_PROP_ROLL          =...,
    CV_CAP_PROP_IRIS          =...,
    CV_CAP_PROP_SETTINGS      =...,
    CV_CAP_PROP_BUFFERSIZE    =...,

    CV_CAP_PROP_AUTOGRAB      =..., // property for videoio class CvCapture_Android only
    CV_CAP_PROP_SUPPORTED_PREVIEW_SIZES_STRING=..., // readonly, tricky property, returns cpnst char* indeed
    CV_CAP_PROP_PREVIEW_FORMAT=..., // readonly, tricky property, returns cpnst char* indeed

    // OpenNI map generators
    CV_CAP_OPENNI_DEPTH_GENERATOR =...,
    CV_CAP_OPENNI_IMAGE_GENERATOR =...,
    CV_CAP_OPENNI_GENERATORS_MASK =...,

    // Properties of cameras available through OpenNI interfaces
    CV_CAP_PROP_OPENNI_OUTPUT_MODE     =...,
    CV_CAP_PROP_OPENNI_FRAME_MAX_DEPTH =..., // in mm
    CV_CAP_PROP_OPENNI_BASELINE        =..., // in mm
    CV_CAP_PROP_OPENNI_FOCAL_LENGTH    =..., // in pixels
    CV_CAP_PROP_OPENNI_REGISTRATION    =..., // flag
    CV_CAP_PROP_OPENNI_REGISTRATION_ON =..., // flag that synchronizes the remapping depth map to image map
                                                                          // by changing depth generator's view point (if the flag is "on") or
                                                                          // sets this view point to its normal one (if the flag is "off").
    CV_CAP_PROP_OPENNI_APPROX_FRAME_SYNC =...,
    CV_CAP_PROP_OPENNI_MAX_BUFFER_SIZE   =...,
    CV_CAP_PROP_OPENNI_CIRCLE_BUFFER     =...,
    CV_CAP_PROP_OPENNI_MAX_TIME_DURATION =...,

    CV_CAP_PROP_OPENNI_GENERATOR_PRESENT =...,
    CV_CAP_PROP_OPENNI2_SYNC =...,
    CV_CAP_PROP_OPENNI2_MIRROR =...,

    CV_CAP_OPENNI_IMAGE_GENERATOR_PRESENT         =...,
    CV_CAP_OPENNI_IMAGE_GENERATOR_OUTPUT_MODE     =...,
    CV_CAP_OPENNI_DEPTH_GENERATOR_BASELINE        =...,
    CV_CAP_OPENNI_DEPTH_GENERATOR_FOCAL_LENGTH    =...,
    CV_CAP_OPENNI_DEPTH_GENERATOR_REGISTRATION    =...,
    CV_CAP_OPENNI_DEPTH_GENERATOR_REGISTRATION_ON =...,

    // Properties of cameras available through GStreamer interface
    CV_CAP_GSTREAMER_QUEUE_LENGTH           =..., // default is 1

    // PVAPI
    CV_CAP_PROP_PVAPI_MULTICASTIP           =..., // ip for anable multicast master mode. 0 for disable multicast
    CV_CAP_PROP_PVAPI_FRAMESTARTTRIGGERMODE =..., // FrameStartTriggerMode: Determines how a frame is initiated
    CV_CAP_PROP_PVAPI_DECIMATIONHORIZONTAL  =..., // Horizontal sub-sampling of the image
    CV_CAP_PROP_PVAPI_DECIMATIONVERTICAL    =..., // Vertical sub-sampling of the image
    CV_CAP_PROP_PVAPI_BINNINGX              =..., // Horizontal binning factor
    CV_CAP_PROP_PVAPI_BINNINGY              =..., // Vertical binning factor
    CV_CAP_PROP_PVAPI_PIXELFORMAT           =..., // Pixel format

    // Properties of cameras available through XIMEA SDK interface
    CV_CAP_PROP_XI_DOWNSAMPLING  =...,      // Change image resolution by binning or skipping.
    CV_CAP_PROP_XI_DATA_FORMAT   =...,       // Output data format.
    CV_CAP_PROP_XI_OFFSET_X      =...,      // Horizontal offset from the origin to the area of interest (in pixels).
    CV_CAP_PROP_XI_OFFSET_Y      =...,      // Vertical offset from the origin to the area of interest (in pixels).
    CV_CAP_PROP_XI_TRG_SOURCE    =...,      // Defines source of trigger.
    CV_CAP_PROP_XI_TRG_SOFTWARE  =...,      // Generates an internal trigger. PRM_TRG_SOURCE must be set to TRG_SOFTWARE.
    CV_CAP_PROP_XI_GPI_SELECTOR  =...,      // Selects general purpose input
    CV_CAP_PROP_XI_GPI_MODE      =...,      // Set general purpose input mode
    CV_CAP_PROP_XI_GPI_LEVEL     =...,      // Get general purpose level
    CV_CAP_PROP_XI_GPO_SELECTOR  =...,      // Selects general purpose output
    CV_CAP_PROP_XI_GPO_MODE      =...,      // Set general purpose output mode
    CV_CAP_PROP_XI_LED_SELECTOR  =...,      // Selects camera signalling LED
    CV_CAP_PROP_XI_LED_MODE      =...,      // Define camera signalling LED functionality
    CV_CAP_PROP_XI_MANUAL_WB     =...,      // Calculates White Balance(must be called during acquisition)
    CV_CAP_PROP_XI_AUTO_WB       =...,      // Automatic white balance
    CV_CAP_PROP_XI_AEAG          =...,      // Automatic exposure/gain
    CV_CAP_PROP_XI_EXP_PRIORITY  =...,      // Exposure priority (0.5 - exposure 50%, gain 50%).
    CV_CAP_PROP_XI_AE_MAX_LIMIT  =...,      // Maximum limit of exposure in AEAG procedure
    CV_CAP_PROP_XI_AG_MAX_LIMIT  =...,      // Maximum limit of gain in AEAG procedure
    CV_CAP_PROP_XI_AEAG_LEVEL    =...,       // Average intensity of output signal AEAG should achieve(in %)
    CV_CAP_PROP_XI_TIMEOUT       =...,       // Image capture timeout in milliseconds

    // Properties for Android cameras
    CV_CAP_PROP_ANDROID_FLASH_MODE =...,
    CV_CAP_PROP_ANDROID_FOCUS_MODE =...,
    CV_CAP_PROP_ANDROID_WHITE_BALANCE =...,
    CV_CAP_PROP_ANDROID_ANTIBANDING =...,
    CV_CAP_PROP_ANDROID_FOCAL_LENGTH =...,
    CV_CAP_PROP_ANDROID_FOCUS_DISTANCE_NEAR =...,
    CV_CAP_PROP_ANDROID_FOCUS_DISTANCE_OPTIMAL =...,
    CV_CAP_PROP_ANDROID_FOCUS_DISTANCE_FAR =...,
    CV_CAP_PROP_ANDROID_EXPOSE_LOCK =...,
    CV_CAP_PROP_ANDROID_WHITEBALANCE_LOCK =...,

    // Properties of cameras available through AVFOUNDATION interface
    CV_CAP_PROP_IOS_DEVICE_FOCUS =...,
    CV_CAP_PROP_IOS_DEVICE_EXPOSURE =...,
    CV_CAP_PROP_IOS_DEVICE_FLASH =...,
    CV_CAP_PROP_IOS_DEVICE_WHITEBALANCE =...,
    CV_CAP_PROP_IOS_DEVICE_TORCH =...,

    // Properties of cameras available through Smartek Giganetix Ethernet Vision interface
    /* --- Vladimir Litvinenko (litvinenko.vladimir@gmail.com) --- */
    CV_CAP_PROP_GIGA_FRAME_OFFSET_X =...,
    CV_CAP_PROP_GIGA_FRAME_OFFSET_Y =...,
    CV_CAP_PROP_GIGA_FRAME_WIDTH_MAX =...,
    CV_CAP_PROP_GIGA_FRAME_HEIGH_MAX =...,
    CV_CAP_PROP_GIGA_FRAME_SENS_WIDTH =...,
    CV_CAP_PROP_GIGA_FRAME_SENS_HEIGH =...,

    CV_CAP_PROP_INTELPERC_PROFILE_COUNT               =...,
    CV_CAP_PROP_INTELPERC_PROFILE_IDX                 =...,
    CV_CAP_PROP_INTELPERC_DEPTH_LOW_CONFIDENCE_VALUE  =...,
    CV_CAP_PROP_INTELPERC_DEPTH_SATURATION_VALUE      =...,
    CV_CAP_PROP_INTELPERC_DEPTH_CONFIDENCE_THRESHOLD  =...,
    CV_CAP_PROP_INTELPERC_DEPTH_FOCAL_LENGTH_HORZ     =...,
    CV_CAP_PROP_INTELPERC_DEPTH_FOCAL_LENGTH_VERT     =...,

    // Intel PerC streams
    CV_CAP_INTELPERC_DEPTH_GENERATOR =...,
    CV_CAP_INTELPERC_IMAGE_GENERATOR =...,
    CV_CAP_INTELPERC_GENERATORS_MASK =...
};

typedef struct _IplImage IplImage;
typedef struct _IplTileInfo IplTileInfo;
typedef struct _IplROI IplROI;


typedef IplImage* (* Cv_iplCreateImageHeader)
                            (int,int,int,char*,char*,int,int,int,int,int,
                            IplROI*,IplImage*,void*,IplTileInfo*);
typedef void (* Cv_iplAllocateImageData)(IplImage*,int,int);
typedef void (* Cv_iplDeallocate)(IplImage*,int);
typedef IplROI* (* Cv_iplCreateROI)(int,int,int,int,int);
typedef IplImage* (* Cv_iplCloneImage)(const IplImage*);

/* Just a combination of cvGrabFrame and cvRetrieveFrame
!!!DO NOT RELEASE or MODIFY the retrieved frame!!!      */
IplImage* cvQueryFrame( CvCapture* capture );

/* "black box" video file writer structure */
typedef struct CvVideoWriter CvVideoWriter;

/* initialize video file writer */
CvVideoWriter* cvCreateVideoWriter( const char* filename, int fourcc,
                                           double fps, CvSize frame_size,
                                           int is_color );

/* write frame to video file */
CVAPI(int) cvWriteFrame( CvVideoWriter* writer, const IplImage* image );

/* close video file writer */
CVAPI(void) cvReleaseVideoWriter( CvVideoWriter** writer );

/* create window */
CVAPI(int) cvNamedWindow( const char* name, int flags CV_DEFAULT(CV_WINDOW_AUTOSIZE) );

/* Set and Get Property of the window */
CVAPI(void) cvSetWindowProperty(const char* name, int prop_id, double prop_value);
CVAPI(double) cvGetWindowProperty(const char* name, int prop_id);

/* display image within window (highgui windows remember their content) */
CVAPI(void) cvShowImage( const char* name, const CvArr* image );

/* resize/move window */
CVAPI(void) cvResizeWindow( const char* name, int width, int height );
CVAPI(void) cvMoveWindow( const char* name, int x, int y );


/* destroy window and all the trackers associated with it */
CVAPI(void) cvDestroyWindow( const char* name );

CVAPI(void) cvDestroyAllWindows(void);

/* get native window handle (HWND in case of Win32 and Widget in case of X Window) */
CVAPI(void*) cvGetWindowHandle( const char* name );

/* get name of highgui window given its native handle */
CVAPI(const char*) cvGetWindowName( void* window_handle );

/* wait for key event infinitely (delay<=0) or for "delay" milliseconds */
CVAPI(int) cvWaitKey(int delay CV_DEFAULT(0));

enum { CV_WINDOW_AUTOSIZE=... };


/****************************************************************************************\
*                         Haar-like Object Detection functions                           *
\****************************************************************************************/


typedef struct CvHaarClassifierCascade { ...;  } CvHaarClassifierCascade;

/* Loads haar classifier cascade from a directory.
   It is obsolete: convert your cascade to xml and use cvLoad instead */
CVAPI(CvHaarClassifierCascade*) cvLoadHaarClassifierCascade(
                    const char* directory, CvSize orig_window_size);

CVAPI(void) cvReleaseHaarClassifierCascade( CvHaarClassifierCascade** cascade );

#define CV_HAAR_DO_CANNY_PRUNING    1
#define CV_HAAR_SCALE_IMAGE         2
#define CV_HAAR_FIND_BIGGEST_OBJECT 4
#define CV_HAAR_DO_ROUGH_SEARCH     8

CVAPI(CvSeq*) cvHaarDetectObjects( const CvArr* image,
                     CvHaarClassifierCascade* cascade, CvMemStorage* storage,
                     double scale_factor CV_DEFAULT(1.1),
                     int min_neighbors CV_DEFAULT(3), int flags CV_DEFAULT(0),
                     CvSize min_size , CvSize max_size );

/* sets images for haar classifier cascade */
CVAPI(void) cvSetImagesForHaarClassifierCascade( CvHaarClassifierCascade* cascade,
                                                const CvArr* sum, const CvArr* sqsum,
                                                const CvArr* tilted_sum, double scale );

/* runs the cascade on the specified window */
CVAPI(int) cvRunHaarClassifierCascade( const CvHaarClassifierCascade* cascade,
                                       CvPoint pt, int start_stage CV_DEFAULT(0));
    """,
        ),
    ),
)


if __name__ == "__main__":
    ffi.compile()
