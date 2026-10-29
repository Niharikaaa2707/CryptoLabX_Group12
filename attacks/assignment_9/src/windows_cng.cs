
using System;
using System.IO;
using System.Security.Cryptography;

class WindowsCNG
{
    static void Main(string[] args)
    {
        string output = args.Length > 0
            ? args[0]
            : "windows_cng.bin";

        byte[] data = new byte[1024 * 1024];

        RandomNumberGenerator.Fill(data);

        File.WriteAllBytes(output, data);

        Console.WriteLine("Generated 1 MB of random data.");
        Console.WriteLine("Output file: " + output);
        Console.WriteLine("Bytes written: " + data.Length);
    }
}

