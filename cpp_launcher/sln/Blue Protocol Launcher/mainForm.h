#pragma once
#include <iostream>
#include <string>
#include <windows.h>
#include <cstdlib>
#include <fstream>
#include <thread>
#include <msclr/marshal.h>  // Needed to convert String^ to std::string
#include <msclr/marshal_cppstd.h>

namespace BlueProtocolLauncher {

	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	using namespace msclr::interop; // Needed to convert String^ to std::string
	using namespace System::IO; //Needed for input output of textfiles for BP path
	using namespace System::Collections::Generic; //For Lists

	//using namespace System::Runtime::InteropServices; //IMPORTANT FOR CONVERSION OF STRING TO PVOID

	public ref class mainForm : public System::Windows::Forms::Form
	{
	public:
		mainForm(void)
		{
			InitializeComponent(); 
		}

	protected:
		~mainForm()
		{
			if (components)
			{
				delete components;
			}
		}	private: System::Windows::Forms::Button^ button1;

	protected:

	private:
		System::ComponentModel::Container ^components;

#pragma region Windows Form Designer generated code

		void InitializeComponent(void)
		{
			System::ComponentModel::ComponentResourceManager^ resources = (gcnew System::ComponentModel::ComponentResourceManager(mainForm::typeid));
			this->button1 = (gcnew System::Windows::Forms::Button());
			this->SuspendLayout();
			// 
			// button1
			// 
			this->button1->Location = System::Drawing::Point(340, 275);
			this->button1->Name = L"button1";
			this->button1->Size = System::Drawing::Size(300, 100);
			this->button1->TabIndex = 0;
			this->button1->UseVisualStyleBackColor = true;
			this->button1->Click += gcnew System::EventHandler(this, &mainForm::button1_Click);
			// 
			// mainForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 13);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(1000, 600);
			this->Controls->Add(this->button1);
			this->Icon = gcnew System::Drawing::Icon("download.ico");
			this->Name = L"mainForm";
			this->Text = L"Blue Protocol Launcher";
			this->Load += gcnew System::EventHandler(this, &mainForm::mainForm_Load);
			this->ResizeBegin += gcnew System::EventHandler(this, &mainForm::mainForm_ResizeBegin);
			this->ResizeEnd += gcnew System::EventHandler(this, &mainForm::mainForm_ResizeEnd);
			this->ResumeLayout(false);

			this->BackgroundImage = Image::FromFile("xBPuc1u.jpg");
			this->BackgroundImageLayout = ImageLayout::Stretch;
			this->button1->BackgroundImage = Image::FromFile("Blue-Protocol-image2.jpg");
			this->button1->BackgroundImageLayout = ImageLayout::Stretch;
		}
#pragma endregion
	private: System::Void button1_Click(System::Object^ sender, System::EventArgs^ e) {

		std::string path;
		bool pathExists = false;

		if (File::Exists("path.txt"))
		{
			StreamReader read("path.txt");
			path = marshal_as<std::string>(read.ReadToEnd());
			read.Close();
			pathExists = true;
		}
		else if (File::Exists("C:\\Program Files (x86)\\Bandai Namco Entertainment\\BLUEPROTOCOL\\BLUEPROTOCOL.exe"))
		{
			path = "C:\\Program Files (x86)\\Bandai Namco Entertainment\\BLUEPROTOCOL\\BLUEPROTOCOL.exe";
			pathExists = true;
		}
		else
		{
			pathExists = false;
			MessageBox::Show("Please select path for first time initiation.");
		}
		

		OpenFileDialog^ openFileDialog = gcnew OpenFileDialog();

		openFileDialog->Title = "Select Blue Protocol Executable";
		openFileDialog->Filter = "All Files (*.*)|*.*";		
		openFileDialog->CheckFileExists = true;
		openFileDialog->CheckPathExists = true;

		while (!pathExists)
		{
			if (openFileDialog->ShowDialog() == System::Windows::Forms::DialogResult::OK)
			{
				String^ filename = openFileDialog->FileName;
				if (filename->Contains("BLUEPROTOCOL.exe"))
				{
					MessageBox::Show("File Path Saved.");
					path = marshal_as<std::string>(filename);
					StreamWriter write("path.txt");
					array<String^>^ paths = filename->Split('\\');
					write.Write(paths[0]);
					for (int i = 1; i < paths->Length; i++)
					{
						write.Write("\\\\" + paths[i]);
					}
					write.Close();
					pathExists = true;
				}
				else
				{
					MessageBox::Show("Please select Blue Protocol.exe");
				}
			}
			else
			{
				break;
			}
		}


		STARTUPINFOA si{};
		PROCESS_INFORMATION pi{};

		ZeroMemory(&si, sizeof(si));
		ZeroMemory(&pi, sizeof(pi));

		CreateProcessA(NULL, (LPSTR) path.c_str(), NULL, FALSE, NULL, 0, NULL, NULL, &si, &pi);

		CloseHandle(pi.hProcess);
		CloseHandle(pi.hThread);

		Application::Exit();


		/*

		filename->Substring(filename->IndexOf('.')) == ".exe"

		path = "E:\\Blue Protocol\\BLUEPROTOCOL\\BLUEPROTOCOL.exe";

		path = "C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2304.26.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe";
		String^ path1 = msclr::interop::marshal_as<String^>(path);
		LPSTR gamePath = static_cast<LPSTR>(static_cast<PVOID>(Marshal::StringToHGlobalAnsi(path1)));

		path = "Z:\\Steam\\steam.exe";
		 

		
		STARTUPINFO startupInfo = { sizeof(startupInfo) };
		PROCESS_INFORMATION processInfo;

		BOOL result = CreateProcess(
			NULL,                // Application name (use NULL to use programPath)
			path,                // Command line
			NULL,                // Process attributes
			NULL,                // Thread attributes
			FALSE,               // Inherit handles
			0,                   // Creation flags
			NULL,                // Environment (use NULL for current process environment)
			NULL,                // Current directory (use NULL for current process directory)
			&startupInfo,        // Startup info
			&processInfo         // Process info
		);

		if (result) {
			this->textBox1->Text = "Succeeded.";
			//CloseHandle(processInfo.hProcess);
			//CloseHandle(processInfo.hThread);
		}
		else {
			this->textBox1->Text = "Failed.";
		}*/
		
	}
	private: System::Void textBox1_TextChanged(System::Object^ sender, System::EventArgs^ e) {
	}
	private: System::Void mainForm_Load(System::Object^ sender, System::EventArgs^ e) {
	}
private: System::Void mainForm_ResizeBegin(System::Object^ sender, System::EventArgs^ e) {
	//button1->Location = Point((this->Width - 108) / 2, (this->Height - 25) / 2);
}
private: System::Void mainForm_ResizeEnd(System::Object^ sender, System::EventArgs^ e) {
	//button1->Location = Point((this->Width - 108) / 2, (this->Height - 25) / 2);
}
};
}
