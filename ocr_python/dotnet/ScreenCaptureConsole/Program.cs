using SharpDX.Direct3D11;
using System;
using Windows.Graphics.Capture;
using Windows.Graphics.DirectX.Direct3D11;

namespace ScreenCaptureApp
{
    class Program
    {
        static void Main(string[] args)
        {
            // Create Direct3D11 Device.
            using var device = new Device(SharpDX.Direct3D.DriverType.Hardware, DeviceCreationFlags.BgraSupport);
            var dxgiDevice = device.QueryInterface<SharpDX.DXGI.Device>();
            var device3 = Direct3D11Device.FromDXGIDevice(dxgiDevice);

            // Create GraphicsCaptureItem (here you need to provide your capture item).
            GraphicsCaptureItem captureItem = ...; // Needs to be implemented, see the note below.
            IntPtr windowHandle = ...; // Handle to the window you want to capture.

            // Initialize the screen capture.
            using var capture = new BasicCapture(device3, captureItem, windowHandle);
            capture.StartCapture();

            // Now the capture has started, the captured screen will be stored in capture.array.
            // You can access this in your code and process it further, e.g. save it to a file.
        }
    }
}
