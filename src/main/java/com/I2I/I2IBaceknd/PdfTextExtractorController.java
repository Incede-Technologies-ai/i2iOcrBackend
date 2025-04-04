package com.I2I.I2IBaceknd;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.*;

@RestController
@RequestMapping("/extract")
@CrossOrigin(origins = "http://localhost:30014")
public class PdfTextExtractorController {

    @GetMapping("/text")
    public String extractTextFromPdf(@RequestParam String pdfPath) {
        try {
            System.out.println("Received PDF Path: " + pdfPath);

            // ✅ Absolute path to extract_text.py
            String pythonScript = "C:\\Users\\user\\Desktop\\my project\\I2IBaceknd\\src\\main\\java\\com\\I2I\\I2IBaceknd\\extract_text.py";

            // ✅ Ensure file exists
            File file = new File(pdfPath);
            if (!file.exists()) {
                return "Error: PDF file not found -> " + pdfPath;
            }

            // ✅ ProcessBuilder to run Python script
            ProcessBuilder processBuilder = new ProcessBuilder("python", pythonScript, pdfPath);
            processBuilder.redirectErrorStream(true); // Capture errors in output

            // ✅ Start Process
            Process process = processBuilder.start();

            // ✅ Read Process Output
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(), "UTF-8"))) {
                StringBuilder output = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line).append("\n");
                }

                // ✅ Wait for process to complete
                process.waitFor();

                // ✅ Print Extracted Text
                System.out.println("Extracted Text:\n" + output);

                // ✅ Delete the PDF file after processing
                if (deleteFile(pdfPath)) {
                    System.out.println("Deleted File: " + pdfPath);
                } else {
                    System.out.println("Failed to delete: " + pdfPath);
                }

                return output.toString().trim();
            }
        } catch (Exception e) {
            e.printStackTrace();
            return "Error extracting text: " + e.getMessage();
        }
    }

    // ✅ Method to delete the file
    private boolean deleteFile(String filePath) {
        File file = new File(filePath);
        if (file.exists()) {
            return file.delete();
        }
        return false;
    }
}
