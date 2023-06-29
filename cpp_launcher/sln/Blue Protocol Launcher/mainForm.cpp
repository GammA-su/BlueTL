#include "mainForm.h"
#include <Windows.h>
#include <vcclr.h>
#include <iostream>

using namespace BlueProtocolLauncher;
using namespace System;
using namespace System::Windows::Forms;

[STAThread]
int main()
{
	Application::SetCompatibleTextRenderingDefault(false);
	Application::EnableVisualStyles(); 

	Application::Run(gcnew mainForm());
	return 0;
}