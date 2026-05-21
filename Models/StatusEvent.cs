namespace ImmiAccount.Models;

public class StatusEvent
{
    public int Id { get; set; }
    public string ApplicationId { get; set; } = "";
    public string StatusCode { get; set; } = "";
    public string OccurredAt { get; set; } = "";
    public string? SourceSystem { get; set; }
}
