namespace ImmiAccount.Models;

public class Correspondence
{
    public int Id { get; set; }
    public string ApplicationId { get; set; } = "";
    public string Title { get; set; } = "";
    public string DateSent { get; set; } = "";
    public string RecipientEmail { get; set; } = "";
    public string? Body { get; set; }
}
