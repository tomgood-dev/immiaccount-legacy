namespace ImmiAccount.Models;

public class User
{
    public int Id { get; set; }
    public string Username { get; set; } = "";
    public string Password { get; set; } = "";
    public string DisplayName { get; set; } = "";
    public string FamilyName { get; set; } = "";
    public string GivenNames { get; set; } = "";
    public string DateOfBirth { get; set; } = "";
    public string Email { get; set; } = "";
    public string? Phone { get; set; }
    public string? AgentEmail { get; set; }
}
