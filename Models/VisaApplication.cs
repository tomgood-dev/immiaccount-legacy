namespace ImmiAccount.Models;

public class VisaApplication
{
    public string Id { get; set; } = "";
    public int ApplicantId { get; set; }
    public string SubclassCode { get; set; } = "";
    public string ReferenceNumber { get; set; } = "";
    public string DateLodged { get; set; } = "";
    public string LastUpdated { get; set; } = "";
    public string CurrentStatus { get; set; } = "";
    public string? SponsorName { get; set; }

    public User? Applicant { get; set; }
    public VisaSubclass? Subclass { get; set; }
}
