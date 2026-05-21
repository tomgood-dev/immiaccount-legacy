namespace ImmiAccount.Models;

public class Document
{
    public int Id { get; set; }
    public string ApplicationId { get; set; } = "";
    public string Filename { get; set; } = "";
    public long SizeBytes { get; set; }
    public string DocumentType { get; set; } = "";
    public string UploadedAt { get; set; } = "";
}
