namespace ImmiAccount.Models;

public class Payment
{
    public int Id { get; set; }
    public string? ApplicationId { get; set; }
    public decimal AmountAud { get; set; }
    public string? Method { get; set; }
    public string? GatewayRef { get; set; }
    public string? PaidAt { get; set; }
    public string Status { get; set; } = "";
    public string? Type { get; set; }
    public string? IssuingOffice { get; set; }
    public string Currency { get; set; } = "AUD";

    public VisaApplication? Application { get; set; }
}
