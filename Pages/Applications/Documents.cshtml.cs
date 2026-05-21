using ImmiAccount.Data;
using ImmiAccount.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace ImmiAccount.Pages.Applications;

public class DocumentsModel : PageModelBase
{
    private readonly AppDbContext _db;
    private const long MaxUploadBytes = 5 * 1024 * 1024;

    public DocumentsModel(AppDbContext db) => _db = db;

    public List<Document> Documents { get; set; } = new();
    public bool UploadSuccess { get; set; }
    public string[] DocumentTypes { get; } =
    [
        "Passport", "Birth Certificate", "Employment Contract", "Skills Assessment",
        "Police Clearance", "Health Certificate", "Qualifications",
        "Identity Document", "Sponsorship Documents", "Other"
    ];

    public IActionResult OnGet(string appId)
    {
        var redirect = CheckAuth();
        if (redirect != null) return redirect;

        if (!ApplicationExists(appId)) return RedirectToPage("/Applications/Index");

        LoadDocuments(appId);
        SetViewData(appId);
        return Page();
    }

    public IActionResult OnPost(string appId, IFormFile? documentFile, string documentType = "Other")
    {
        var redirect = CheckAuth();
        if (redirect != null) return redirect;

        if (!ApplicationExists(appId)) return RedirectToPage("/Applications/Index");

        if (documentFile != null && documentFile.Length > 0 && documentFile.Length <= MaxUploadBytes)
        {
            var safeName = documentFile.FileName.Replace("/", "_").Replace("\\", "_");
            _db.Documents.Add(new Document
            {
                ApplicationId = appId,
                Filename = safeName,
                SizeBytes = documentFile.Length,
                DocumentType = documentType,
                UploadedAt = DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")
            });
            _db.SaveChanges();
            UploadSuccess = true;
        }
        // Files > 5MB are silently dropped — intentional legacy bug

        LoadDocuments(appId);
        SetViewData(appId);
        return Page();
    }

    private bool ApplicationExists(string appId) =>
        _db.Applications.Any(a => a.Id == appId && a.ApplicantId == CurrentUserId!.Value);

    private void LoadDocuments(string appId) =>
        Documents = _db.Documents
            .Where(d => d.ApplicationId == appId)
            .OrderByDescending(d => d.UploadedAt)
            .ToList();

    private void SetViewData(string appId)
    {
        var app = _db.Applications.Include(a => a.Subclass).First(a => a.Id == appId);
        ViewData["AppId"] = appId;
        ViewData["ActiveTab"] = "documents";
        ViewData["AppReference"] = app.ReferenceNumber;
        ViewData["AppSubclassName"] = app.Subclass!.Name;
        ViewData["Title"] = $"Documents - {app.ReferenceNumber}";
    }
}
